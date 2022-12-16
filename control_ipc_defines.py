
from enum import Enum

# defines from file: ipc_control.h
MAX_MESSAGE_SIZE = 254
RSRC_STRING_LENGTH = 4
RSRC_OFFSET = 4
HEADER_LENGTH = 8
GET_METHOD = "GET"
PUT_METHOD = "PUT"
RSP_METHOD = "RSP"
STAT_RSRC = "STAT"
STOP_RSRC = "STOP"
STRT_RSRC = "STRT"
PAUS_RSRC = "PAUS"
MODE_RSRC = "MODE"
BCFG_RSRC = "BCFG" #config params that apply to both drill & game: Level, TrashTalk, Grunt
DCFG_RSRC = "DCFG" #config params that apply to drills: speed_mod, delay_mod, elevator_mod
GCFG_RSRC = "GCFG" #config params that apply to games:
SCOR_RSRC = "SCOR" #player scores
IPCS_RSRC = "IPCS" #game IPC statistics
FLTS_RSRC = "FLTS" #list of faults
FUNC_RSRC = "FUNC" #used to call functions, like creep
class base_mode_e(Enum):
  BASE_MODE_NONE = 0
  GAME = 1
  DRILL = 2
  BEEP = 3
  WORKOUT = 4
  CREEP_CALIBRATION = 5
class base_state_e(Enum):
  BASE_STATE_NONE = 0
  IDLE = 1
  ACTIVE = 2
  PAUSED = 3
  FAULTED = 4
  OUTOFBALLS = 5
class soft_fault_e(Enum):
  SOFT_FAULT_NONE = 0
  SOFT_FAULT_TRACKING = 1
STATUS_PARAM = "status"
SOFT_FAULT_PARAM = "sFault"
HARD_FAULT_PARAM = "hFault"
MODE_PARAM = "mode"
ID_PARAM = "id" #drill or workout ID
STEP_PARAM = "step" #drill step to execture
LEVEL_PARAM = "level"
TRASHT_PARAM = "trash" #trash talking boolean
GRUNTS_PARAM = "grunts"
SPEED_MOD_PARAM = "speed"
DELAY_MOD_PARAM = "delay"
ELEVATION_MOD_PARAM = "eleva"
POINTS_DELAY_PARAM = "ptDelay" #increase/decrease time between points in seconds
TIEBREAKER_PARAM = "tiebreaker"
RUN_REDUCE_PARAM = "reduceRun" #reduce running - not in initial release
SERVE_MODE_PARAM = "wServes" #server for game: No Serves, All Serves, Alternative Serves
class serve_mode_e(Enum):
  ALTERNATE_SERVES = 0
  PLAYER_ALL_SERVES = 1
  BOOMER_ALL_SERVES = 2
FLT_CODE_PARAM = "fCod"
FLT_LOCATION_PARAM = "fLoc"
FLT_TIMESTAMP_PARAM = "fTim"
GAME_START_TIME = "time"
SERVER = "server"
BOOMER_SETS_PARAM = "b_sets"
PLAYER_SETS_PARAM = "p_sets"
BOOMER_GAMES_PARAM = "b_games"
PLAYER_GAMES_PARAM = "p_games"
BOOMER_POINTS_PARAM = "b_pts"
PLAYER_POINTS_PARAM = "p_pts"
BOOMER_TIEPOINTS_PARAM = "b_t_pts"
PLAYER_TIEPOINTS_PARAM = "p_t_pts"
IPC_0_NUM_READS_PARAM = "0_rd"
IPC_0_NUM_WRITES_PARAM = "0_wr"
IPC_0_NUM_BAD_PARAM = "0_bad"
IPC_1_NUM_READS_PARAM = "1_rd"
IPC_1_NUM_WRITES_PARAM = "1_wr"
IPC_1_NUM_BAD_PARAM = "1_bad"
FUNC_CREEP = "creep" #creep is the key, the value can be Elevator or Rotory
FUNC_RESTART = "restart" #value can be either c for cams or a for base+cams
FUNC_DUMP = "dump" #values: c==cam stats; t==tach stats; n==net error stats
FUNC_GEN_CORRECTION_VECTORS = "gen_cv" #value is 0 or 1 for cam number
FUNC_TRACKING = "tracking" #value is either begin or end
RESP_OK = 200
BAD_REQUEST = 400 #used if the message decode fails
FORBIDDEN = 403
NOT_FOUND = 404 # unknown resource
METHOD_NOT_ALLOWED = 405
LOCKED = 423 # used for PUT mode if the boomer_base is Active
UNPROCESSABLE_ENTITY = 422 #used for encode errors - there was not a great error response for this
INTERNAL_SERVER_ERROR = 500 #used when the request fails (e.g. correction vector generation)
CTRL_TRANSPRT = 0
UI_TRANSPRT = 1
BASE_NAME = "Base"
CTRL_NAME = "Ctrl"
UI_NAME = "Ui"

# defines from file: level_setting.h
SAME_LEVEL_AS_BOOMER = 11
EASIER_LEVEL_THAN_BOOMER = 12
HARDER_LEVEL_THAN_BOOMER = 13
LEVEL_MIN = 20
LEVEL_MAX = 70
LEVEL_DEFAULT = 35
LEVEL_STEP = 5 #Dave wants to be to change this at a finer scale than presented to a user
LEVEL_UI_STEP = 5
LEVEL_UI_FACTOR = 10 #the UI would divide the min/max/default & ui_step by this number to present to the user

# defines from file: calc_ball.h
class balltype_e(Enum):
  NONE = 0
  SERVE = 1
  DROP = 2
  FLAT = 3
  LOOP = 4
  CHIP = 5
  LOB = 6
  TOPSPIN = 7
  PASS = 8
  CUSTOM = 9
  RAND_GROUND = 10
  RAND_NET = 11
  REPEAT = 12
  END = 13
ROTARY_CALIB_NAME = "ROTARY"
ROTARY_CALIB_TYPE = 10
ELEVATOR_CALIB_NAME = "ELEVATOR"
ELEVATOR_CALIB_TYPE = (ROTARY_CALIB_TYPE + 1)
class ball_servo_param_e(Enum):
  ELEV = 0
  SPEED = 1
  SPIN = 2
ROTTYPE_F4 = 0
ROTTYPE_F3 = 1
ROTTYPE_F2 = 2
ROTTYPE_F1 = 3
ROTTYPE_CENTER = 4
ROTTYPE_B1 = 5
ROTTYPE_B2 = 6
ROTTYPE_B3 = 7
ROTTYPE_B4 = 8
ROTTYPE_RAND = 9
ROTTYPE_F5 = 10
ROTTYPE_B5 = 11
ROTTYPE_RANDFH = 12
ROTTYPE_RANDBH = 13
ROTTYPE_R2 = 14
ROTTYPE_R3 = 15
ROTTYPE_INV = 16

# defines from file: drill.h
SPEED_BALL_MIN = 20
SPEED_BALL_MAX = 80
SPEED_MOD_MIN = 80
SPEED_MOD_MAX = 120
SPEED_MOD_DEFAULT = 100
SPEED_MOD_STEP = 2
ELEVATION_ANGLE_MOD_MIN = -32
ELEVATION_ANGLE_MOD_MAX = 32
ELEVATION_ANGLE_MOD_DEFAULT = 0
ELEVATION_ANGLE_MOD_STEP = 2
ELEVATION_ANGLE_BALL_MIN = 1.0
ELEVATION_ANGLE_BALL_MAX = 46.0
DELAY_MOD_MIN = -2000
DELAY_MOD_MAX = 2000
DELAY_MOD_DEFAULT = 0
DELAY_MOD_STEP = 100
DELAY_UI_STEP = 100
DELAY_UI_FACTOR = 1000
DELAY_BALL_MIN = 0.75
DELAY_BALL_MAX = 30
SPIN_BALL_MIN = -3000
SPIN_BALL_MAX = 3000

# defines from file: drill_load.h
DRILL_FILES_PATH = "/home/pi/boomer/drills/"
NAME_LINE = 1
DESC_LINE = 2
AUDIO_LINE = 3
COLUMN_TITLES_LINE = 4
BEEP_DRILL_NUMBER_START = 901
BEEP_DRILL_NUMBER_END = 979
THROWER_CALIB_DRILL_NUMBER_START = 781
CALIB_MODE_STRING = "!calibration: "

# defines from file: common_code/fault.h
class fault_e(Enum):
  FAULT_BEGIN = 0
  DEVICE_FAILURE_ON_INIT = 1
  CAM_FAILURE_ON_SET_MODE = 2
  CAM_FAILURE_ON_SET_CONTROL = 3
  CAM_FAILURE_TO_CAPTURE = 4
  CAM_FAILED_PARAMETER_LOAD = 5
  NOT_RECEIVING_FROM_NETWORK_DEVICE = 6
  UNRECOGNIZED_IP = 7
  UNSUPPORTED_COMMAND = 8
  PRIORITY_CAPABILITY_NOT_SET = 9
  UNRECOGNIZED_FAULT_CODE = 10
  UNRECOGNIZED_FAULT_LOCATION = 11
  NOT_RECEIVING_DATA_FROM_CAM = 12
  CAM_SET_GAIN_FAILED = 13
  CAM_SET_EXPOSURE_FAILED = 14
  CAMERAS_NOT_SYNCHRONIZED = 15
  I2C_ERROR_ON_INITIALIZATION = 16
  GPIO_ERROR_ON_INITIALIZATION = 17
  DAC_ERROR_ON_INITIALIZATION = 18
  DAC_WRITE_ERROR = 19
  ADC_ERROR_ON_INITIALIZATION = 20
  ADC_EXCESSIVE_READ_ERRORS = 21
  TACH_ERROR_ON_INITIALIZATION = 22
  TACH_EXCESSIVE_READ_ERRORS = 23
  BALL_SWITCH_STUCK_DOWN = 24
  BOTTOM_WHEEL_FAILED_TO_REACH_SPEED = 25
  TOP_WHEEL_FAILED_TO_REACH_SPEED = 26
  LEFT_RIGHT_FAILED_TO_REACH_TARGET = 27
  UP_DOWN_SERVO_FAILED_TO_REACH_TARGET = 28
  CONTROL_PROGRAM_NOT_RUNNING = 29
  CONTROL_PROGRAM_GET_STATUS_FAILED = 30
  CONTROL_PROGRAM_FAILED = 31
  NOT_TRACKING_BALL = 32
  READ_CAMERA_CONFIG_FILE_ERROR = 33
  CAMERA_VECTOR_GENERATION_FAILED = 34
  SETTING_CAMERA_EXPOSURE_FAILED = 35
  CAMERA_FOCAL_LENGTH_CALC_FAILED = 36
  FAULT_END = 37
class net_device_e(Enum):
  LEFT = 0
  RIGHT = 1
  SPEAKER = 2
  BASE = 3
  TRACKING = 4
  UNRECOGNIZED_DEVICE = 5
