from dataclasses import dataclass
from enum import Enum

class DataType(Enum):
    MATRIX = "MATRIX"
    VECTOR = "VECTOR"
    GROUP = "GROUP"
    SCALAR = "SCALAR"
    WINDOW = "WINDOW"
    INTEGER = "INTEGER"

@dataclass
class OperatorDefinition:
    name: str
    category: str
    inputs: list[str]
    output: DataType
    optional: dict
    variadic: bool = False


OPERATORS = [

    # =====================
    # Arithmetic
    # =====================

    OperatorDefinition(
        name="abs",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="add",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"filter": "false"}
    ),

    OperatorDefinition(
        name="densify",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="divide",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="inverse",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="log",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="max",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={},
        variadic=True
    ),

    OperatorDefinition(
        name="min",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={},
        variadic=True
    ),

    OperatorDefinition(
        name="multiply",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"filter": "false"},
        variadic=True
    ),

    OperatorDefinition(
        name="power",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.SCALAR],
        output=DataType.MATRIX,
        optional={"precise": "false"}
    ),

    OperatorDefinition(
        name="reverse",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="sign",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="signed_power",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.SCALAR],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="sqrt",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="subtract",
        category="ARITHMETIC",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"filter": "false"}
    ),

    # =====================
    # Logical
    # =====================

    OperatorDefinition(
        name="and",
        category="LOGICAL",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="if_else",
        category="LOGICAL",
        inputs=[
            DataType.MATRIX,   # condition
            DataType.MATRIX,   # true value
            DataType.MATRIX    # false value
        ],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="is_nan",
        category="LOGICAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="not",
        category="LOGICAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="or",
        category="LOGICAL",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),
    # =====================
    # Time Series
    # =====================

    OperatorDefinition(
        name="days_from_last_change",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="hump",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"hump": "0.01"}
    ),

    OperatorDefinition(
        name="kth_element",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW, DataType.SCALAR],
        output=DataType.MATRIX,
        optional={"ignore": '"NAN"'}
    ),

    OperatorDefinition(
        name="last_diff_value",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_arg_max",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_arg_min",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_av_diff",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_backfill",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={
            "lookback": "252",
            "k": "1",
            "ignore": '"NAN"'
        }
    ),

    OperatorDefinition(
        name="ts_corr",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_count_nans",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_covariance",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_decay_linear",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={"dense": "false"}
    ),

    OperatorDefinition(
        name="ts_delay",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_delta",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_mean",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_product",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_quantile",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={"driver": '"gaussian"'}
    ),

    OperatorDefinition(
        name="ts_rank",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={"constant": "0"}
    ),

    OperatorDefinition(
        name="ts_regression",
        category="TIME_SERIES",
        inputs=[
            DataType.MATRIX,
            DataType.MATRIX,
            DataType.WINDOW
        ],
        output=DataType.MATRIX,
        optional={
            "lag": "0",
            "rettype": "0"
        }
    ),

    OperatorDefinition(
        name="ts_scale",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={"constant": "0"}
    ),

    OperatorDefinition(
        name="ts_std_dev",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_step",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_sum",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="ts_zscore",
        category="TIME_SERIES",
        inputs=[DataType.MATRIX, DataType.WINDOW],
        output=DataType.MATRIX,
        optional={}
    ),
    # =====================
    # Cross Sectional
    # =====================

    OperatorDefinition(
        name="normalize",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"useStd": "false", "limit": "0.0"}
    ),

    OperatorDefinition(
        name="quantile",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"driver": '"gaussian"', "sigma": "1.0"}
    ),

    OperatorDefinition(
        name="rank",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"rate": "2"}
    ),

    OperatorDefinition(
        name="scale",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={
            "scale": "1",
            "longscale": "1",
            "shortscale": "1"
        }
    ),

    OperatorDefinition(
        name="MATRIX_neut",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX, DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="winsorize",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={"std": "4"}
    ),

    OperatorDefinition(
        name="zscore",
        category="CROSS_SECTIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={}
    ),
    # =====================
    # VECTOR
    # =====================

    OperatorDefinition(
        name="vec_avg",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_sum",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_choose",
        category="VECTOR",
        inputs=[DataType.VECTOR, DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_count",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_ir",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_kurtosis",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_max",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_min",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_norm",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_percentage",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_powersum",
        category="VECTOR",
        inputs=[DataType.VECTOR, DataType.SCALAR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_range",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_skewness",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),

    OperatorDefinition(
        name="vec_stddev",
        category="VECTOR",
        inputs=[DataType.VECTOR],
        output=DataType.VECTOR,
        optional={}
    ),
    # =====================
    # Transformational
    # =====================

    OperatorDefinition(
        name="bucket",
        category="TRANSFORMATIONAL",
        inputs=[DataType.MATRIX],
        output=DataType.MATRIX,
        optional={
            "range": None,
            "buckets": None,
            "skipBegin": "false",
            "skipEnd": "false",
            "skipBoth": "false",
            "NANGroup": "false"
        }
    ),

    OperatorDefinition(
        name="trade_when",
        category="TRANSFORMATIONAL",
        inputs=[
            DataType.MATRIX,   # trigger
            DataType.MATRIX,   # alpha
            DataType.MATRIX    # exit condition
        ],
        output=DataType.MATRIX,
        optional={}
    ),
    # =====================
    # Group
    # =====================

    OperatorDefinition(
        name="group_backfill",
        category="GROUP",
        inputs=[
            DataType.MATRIX,
            DataType.GROUP,
            DataType.WINDOW
        ],
        output=DataType.MATRIX,
        optional={"std": "4.0"}
    ),

    OperatorDefinition(
        name="group_mean",
        category="GROUP",
        inputs=[
            DataType.MATRIX,
            DataType.MATRIX,
            DataType.GROUP
        ],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="group_neutralize",
        category="GROUP",
        inputs=[
            DataType.MATRIX,
            DataType.GROUP
        ],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="group_rank",
        category="GROUP",
        inputs=[
            DataType.MATRIX,
            DataType.GROUP
        ],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="group_scale",
        category="GROUP",
        inputs=[
            DataType.MATRIX,
            DataType.GROUP
        ],
        output=DataType.MATRIX,
        optional={}
    ),

    OperatorDefinition(
        name="group_zscore",
        category="GROUP",
        inputs=[
            DataType.MATRIX,
            DataType.GROUP
        ],
        output=DataType.MATRIX,
        optional={}
    )
]

OPTIONAL_VALUES = {

    "filter": ["true", "false"],

    "driver": [
        '"gaussian"',
        '"uniform"',
        '"cauchy"'
    ],

    "dense": ["true", "false"],

    "precise": ["true", "false"],

    "constant": ["0","1","2"],

    "lag": ["0","1","2"],

    "rettype": ["0","1","2"],

    "ignore": ['"NAN"'],

}