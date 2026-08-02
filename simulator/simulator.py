from parameters import SIMULATION_CRITERIA, DEFAULT_SETTINGS
import csv
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import pandas as pd
import time
from session.session import WQSession

class Simulator:

    def __init__(self, session: WQSession):
        self.session = session

    #알파가 기준을 만족하는지 확인
    def check_alpha_criteria(self, alpha_data):
        passed = True
        fail_reasons = []
        
        # 기본 성능 검증
        if alpha_data['sharpe'] < SIMULATION_CRITERIA['SHARPE_THRESHOLD']:
            fail_reasons.append(f"Sharpe ratio {alpha_data['sharpe']:.3f} < {SIMULATION_CRITERIA['SHARPE_THRESHOLD']}")
            passed = False
            
        # 회전율 검증
        if not (SIMULATION_CRITERIA['TURNOVER_MIN'] <= alpha_data['turnover'] <= SIMULATION_CRITERIA['TURNOVER_MAX']):
            fail_reasons.append(f"Turnover {alpha_data['turnover']:.2f}% not in range [{SIMULATION_CRITERIA['TURNOVER_MIN']}, {SIMULATION_CRITERIA['TURNOVER_MAX']}]")
            passed = False
            
        # Fitness 검증
        if alpha_data['fitness'] < SIMULATION_CRITERIA['FITNESS_THRESHOLD']:
            fail_reasons.append(f"Fitness {alpha_data['fitness']:.3f} < {SIMULATION_CRITERIA['FITNESS_THRESHOLD']}")
            passed = False
            
        # 가중치 검증
        if alpha_data['weight_check'] != 'PASS':
            fail_reasons.append(f"Weight check failed: {alpha_data['weight_check']}")
            passed = False
            
        # Sub-universe Sharpe 검증 (값이 있는 경우에만)
        if alpha_data['subsharpe'] > 0:
            threshold = SIMULATION_CRITERIA['SUBUNIVERSE_SHARPE_RATIO'] * alpha_data['sharpe']
            if alpha_data['subsharpe'] < threshold:
                fail_reasons.append(f"Sub-universe Sharpe {alpha_data['subsharpe']:.3f} < {threshold:.3f}")
                passed = False
        
        if not passed:
            logging.info(f"Alpha failed criteria: {'; '.join(fail_reasons)}")
        else:
            logging.info(f"Alpha PASSED all criteria! Sharpe: {alpha_data['sharpe']:.3f}, Fitness: {alpha_data['fitness']:.3f}, Turnover: {alpha_data['turnover']:.2f}%")
            
        return passed

    #submit_alpha() wait_until_finished() fetch_result evaluate_alpha() save_result() notify_progress() 으로 나누자
    #AlphaGenerator와 SQLiteManager을 새로 설계하여 simulate()은 시뮬엔진 역할만 유지하도록 개선
    def simulate(self, data):
        rows_processed = []
        total_alphas = len(data)
        #알파 하나 처리하는 함수
        def process_simulation(writer, f, simulation):
            if self.session.login_expired: return

            thread = current_thread().name
            alpha = simulation['code'].strip()
            settings = {**DEFAULT_SETTINGS, **simulation}
            #API제출
            logging.info(f"{thread} -- Simulating alpha: {alpha}")
            while True:
                try:
                    r = self.session.post('https://api.worldquantbrain.com/simulations', json={
                        'regular': alpha,
                        'type': 'REGULAR',
                        'settings': {
                            "nanHandling": settings['nanHandling'],
                            "instrumentType": "EQUITY",
                            "delay": settings['delay'],
                            "universe": settings['universe'],
                            "truncation": settings['truncation'],
                            "unitHandling": settings['unitHandling'],
                            "pasteurization": settings['pasteurization'],
                            "region": settings['region'],
                            "language": "FASTEXPR",
                            "decay": settings['decay'],
                            "neutralization": settings['neutralization'],
                            "visualization": False,
                            "maxTrade": settings['maxTrade']
                        }
                    })
                    #바로 결과 안주고 Location을 줘서 그 주소를 계속 조회해야 한다.
                    nxt = r.headers['Location']
                    break
                except:
                    try:
                        if 'credentials' in r.json()['detail']:
                            self.session.login_expired = True
                            return
                    except:
                        logging.info(f'{thread} -- {r.content}')
                        return
                    
            logging.info(f'{thread} -- Obtained simulation link: {nxt}')
            ok = True
            #로깅 개선. 10초마다 Waiting for simulation뜨면 가독성 떨어짐
            while True:
                r = self.session.get(nxt).json()
                if 'alpha' in r:
                    alpha_link = r['alpha']
                    break
                if 'progress' not in r:
                    ok = (False, r.get('message', 'Unknown Error'))
                    break
                time.sleep(10)

            if ok != True:
                logging.info(f'{thread} -- Issue when sending simulation request: {ok[1]}')
                row = [
                    0, settings['delay'], settings['region'],
                    settings['neutralization'], settings['decay'], settings['truncation'],
                    0, 0, 0, 'FAIL', 0, -1, settings['universe'], nxt, alpha
                ]
            else:
                r = self.session.get(f'https://api.worldquantbrain.com/alphas/{alpha_link}').json()
                logging.info(f'{thread} -- Obtained alpha link: https://platform.worldquantbrain.com/alpha/{alpha_link}')
                #결과 파이썬 객체로 제작
                alpha_data = {
                    'sharpe': r['is']['sharpe'],
                    'fitness': r['is']['fitness'],
                    'turnover': r['is']['turnover'],
                    'weight_check': 'PASS',
                    'subsharpe': -1
                }
                #check도 있나보네.
                for check in r['is']['checks']:
                    if check['name'] == 'CONCENTRATED_WEIGHT':
                        alpha_data['weight_check'] = check['result']
                    if check['name'] == 'LOW_SUB_UNIVERSE_SHARPE':
                        alpha_data['subsharpe'] = check['value']
                #여기서 알파 데이터 통과했는지 체크
                passed = self.check_alpha_criteria(alpha_data)
                #csv파일에 저장
                row = [
                    passed, settings['delay'], settings['region'],
                    settings['neutralization'], settings['decay'], settings['truncation'],
                    alpha_data['sharpe'],
                    alpha_data['fitness'],
                    round(100*alpha_data['turnover'], 2),
                    alpha_data['weight_check'],
                    alpha_data['subsharpe'],
                    -1,
                    settings['universe'],
                    f'https://platform.worldquantbrain.com/alpha/{alpha_link}',
                    alpha
                ]
            #writer은 내가 넣어줘야하는거같으네?
            writer.writerow(row)
            f.flush()
            #성공한 알파를 기록한다는데 simulatin이 아까 DEFAULT을 덮어쓴다하지않았나??
            rows_processed.append(simulation)
            
            # 실시간 진행률 표시
            completed = len(rows_processed)
            print(f'\r📈 {completed}/{total_alphas} 알파 시뮬레이션 완료 ({completed/total_alphas*100:.1f}%)', end='', flush=True)
            logging.info(f'{thread} -- Result added to CSV! Progress: {completed}/{total_alphas}')

        #실제 simulation함수 시작부
        try:
            for handler in logging.root.handlers:
                logging.root.removeHandler(handler)
            csv_file = f"data/api_{str(time.time()).replace('.', '_')}.csv"
            logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s: %(message)s', filename=csv_file.replace('csv', 'log'))
            logging.info(f'Creating CSV file: {csv_file}')
            print(f'📊 시뮬레이션 결과 파일: {csv_file}')
            print(f'📋 설정: {DEFAULT_SETTINGS}')
            
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                header = [
                    'passed', 'delay', 'region', 'neutralization', 'decay', 'truncation',
                    'sharpe', 'fitness', 'turnover', 'weight',
                    'subsharpe', 'correlation', 'universe', 'link', 'code'
                ]
                writer.writerow(header)
                #동시에 최대 10개 제출
                with ThreadPoolExecutor(max_workers=10) as executor:
                    _ = executor.map(lambda sim: process_simulation(writer, f, sim), data)
            
            print('\n✅ 시뮬레이션 완료!')
            
            # 🎯 시뮬레이션 결과 요약 출력
            self.print_simulation_summary(csv_file)
            
            print('📊 WorldQuant Brain Alpha Generation System')
        except Exception as e:
            print(f'Issue occurred! {type(e).__name__}: {e}')
        return [sim for sim in data if sim not in rows_processed]


    def print_simulation_summary(self, csv_file):
        """시뮬레이션 결과 요약 출력"""
        try:
            df = pd.read_csv(csv_file)
            
            total_alphas = len(df)
            passed_alphas = len(df[df['passed'] == True])
            failed_alphas = total_alphas - passed_alphas
            pass_rate = (passed_alphas / total_alphas * 100) if total_alphas > 0 else 0
            
            print(f"\n📊 시뮬레이션 결과 요약:")
            print(f"   총 알파 수: {total_alphas}개")
            print(f"   ✅ 통과: {passed_alphas}개 ({pass_rate:.1f}%)")
            print(f"   ❌ 실패: {failed_alphas}개 ({100-pass_rate:.1f}%)")
            
            if passed_alphas > 0:
                passed_df = df[df['passed'] == True]
                avg_sharpe = passed_df['sharpe'].mean()
                avg_fitness = passed_df['fitness'].mean()
                avg_turnover = passed_df['turnover'].mean()
                
                print(f"\n🏆 통과한 알파 평균 성능:")
                print(f"   📈 Sharpe: {avg_sharpe:.3f}")
                print(f"   💪 Fitness: {avg_fitness:.3f}")
                print(f"   🔄 Turnover: {avg_turnover:.2f}%")
                
                # 최고 성능 알파
                best_sharpe_idx = passed_df['sharpe'].idxmax()
                best_alpha = passed_df.loc[best_sharpe_idx]
                print(f"\n⭐ 최고 Sharpe 알파:")
                print(f"   코드: {best_alpha['code'][:80]}...")
                print(f"   Sharpe: {best_alpha['sharpe']:.3f}, Fitness: {best_alpha['fitness']:.3f}")
                print(f"   링크: {best_alpha['link']}")
            
            # 실패 이유 분석 (간단히)
            if failed_alphas > 0:
                failed_df = df[df['passed'] == False]
                print(f"\n❌ 실패한 알파 주요 이슈:")
                low_sharpe = len(failed_df[failed_df['sharpe'] < SIMULATION_CRITERIA['SHARPE_THRESHOLD']])
                low_fitness = len(failed_df[failed_df['fitness'] < SIMULATION_CRITERIA['FITNESS_THRESHOLD']])
                
                if low_sharpe > 0:
                    print(f"   📉 낮은 Sharpe: {low_sharpe}개")
                if low_fitness > 0:
                    print(f"   💔 낮은 Fitness: {low_fitness}개")
                    
        except Exception as e:
            print(f"⚠️ 결과 요약 생성 중 오류: {e}")