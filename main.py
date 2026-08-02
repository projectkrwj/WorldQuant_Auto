import logging
import os

from parameters import DEFAULT_SETTINGS

from session.session import WQSession

from simulator.simulator import Simulator
from simulator.alpha_builder import AlphaBuilder

from database.field_repository import FieldRepository

from generator.generator import Generator
from generator.field_selector import RandomFieldSelector
from generator.operator_selector import RandomOperatorSelector
from generator.parameter_generator import RandomParameterGenerator


# ==========================
# directory
# ==========================

os.makedirs(
    "data",
    exist_ok=True
)

os.makedirs(
    "logs",
    exist_ok=True
)


# ==========================
# logging
# ==========================

for handler in logging.root.handlers:
    logging.root.removeHandler(handler)


logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s: %(message)s"
)



def main():


    # ==========================
    # Database
    # ==========================

    field_repository = FieldRepository(
        "worldquant.db"
    )


    # ==========================
    # Selector / Generator
    # ==========================

    field_selector = RandomFieldSelector(
        field_repository
    )

    operator_selector = RandomOperatorSelector()


    parameter_generator = RandomParameterGenerator()



    generator = Generator(
        operator_selector=operator_selector,
        field_selector=field_selector,
        parameter_generator=parameter_generator,
        max_depth=4
    )


    # ==========================
    # Alpha Builder
    # ==========================

    alpha_builder = AlphaBuilder(
        generator=generator,
        settings=DEFAULT_SETTINGS
    )


    # ==========================
    # Session / Simulator
    # ==========================

    session = WQSession()

    simulator = Simulator(
        session
    )


    # ==========================
    # Generate Alpha
    # ==========================

    alpha = alpha_builder.build()


    logging.info(
        f"Generated Alpha : {alpha['expression']}"
    )


    # ==========================
    # Simulation
    # ==========================

    result = simulator.simulate(
        alpha
    )


    logging.info(
        "Simulation complete"
    )

    print(result)



if __name__ == "__main__":
    main()



'''
import csv
import logging
import requests
import json
import time
import os
import pandas as pd
import argparse
from datetime import datetime
from parameters import SIMULATION_CRITERIA, DEFAULT_SETTINGS
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread
import webbrowser

from session.session import WQSession
from simulator.simulator import Simulator
from database.data import update_all_fields, update_datasets


# 로그 및 데이터 디렉토리 생성
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)
#기존 로깅 제거
for handler in logging.root.handlers:
    logging.root.removeHandler(handler)
#로그 초기화
logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s: %(message)s')

alpha = "rank(ts_mean(close,5))"
simulation_data = []
simulation_data.append({
                    'code': alpha,
                    **DEFAULT_SETTINGS
                })
session = WQSession()
simulator = Simulator(session)
'''


'''
dataset업데이트원할시 실행
update_datasets(session)
update_all_fields(session)
'''

''' generator생성 후 main사용법
from generator import Generator
from generator.selector import RandomSelector
from generator.renderer import render

selector = RandomSelector()

generator = Generator(selector)

ast = generator.generate()

print(render(ast))
'''