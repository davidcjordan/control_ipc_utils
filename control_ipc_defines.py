
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
FUNC_RSRC = "FUNC" #used to call functions, like calibration
SRVO_RSRC = "SRVO" #get/set servo parameters: center_fast, drop_speed, PASS_ANGLE, etc
class base_mode_e(Enum):
  BASE_MODE_NONE = 0
  GAME = 1
  DRILL = 2
  BEEP = 3
  WORKOUT = 4
  CALIBRATION = 5
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
CONTINUOUS_MOD_PARAM = "contin"
POINTS_DELAY_PARAM = "ptDelay" #increase/decrease time between points in seconds
TIEBREAKER_PARAM = "tiebreaker"
RUN_REDUCE_PARAM = "reduceRun" #reduce running - not in initial release
SERVE_MODE_PARAM = "wServes" #server for game: No Serves, All Serves, Alternative Serves
ADVANCED_GAME_PARAM = "advanced" #
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
FUNC_CALIB = "calib" #calib is the key, the value can be Elevator or Rotory or Wheels
FUNC_RESTART = "restart" #value can be either c for cams or a for base+cams
FUNC_DUMP = "dump" #values: c==cam stats; t==tach stats; n==net error stats; f==faults
FUNC_GEN_CORRECTION_VECTORS = "gen_cv" #value is 0 or 1 for cam number
FUNC_TRACKING = "tracking" #value is either begin or end
FUNC_HELP = "help" #values: g==game
CENTER_ANGLE_PARAM = "center"
SERVE_ANGLE_PARAM = "Serve_ang"
FLAT_ANGLE_PARAM = "Flat_ang"
LOOP_ANGLE_PARAM = "Loop_ang"
CHIP_ANGLE_PARAM = "Chip_ang"
TOPSPIN_ANGLE_PARAM = "Top_ang"
PASS_ANGLE_PARAM = "Pass_ang"
DROP_SPEED_PARAM = "drp_sp"
LOB_SPEED_PARAM = "lob_sp"
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
class ball_servo_param_e(Enum):
  ELEV = 0
  SPEED = 1
  SPIN = 2
class rotary_setting_e(Enum):
  ROTTYPE_CENTER = 0
  ROTTYPE_F1 = 1
  ROTTYPE_F2 = 2
  ROTTYPE_F3 = 3
  ROTTYPE_F4 = 4
  ROTTYPE_F5 = 5
  ROTTYPE_F6 = 6
  ROTTYPE_F7 = 7
  ROTTYPE_F8 = 8
  ROTTYPE_F9 = 9
  ROTTYPE_F10 = 10
  ROTTYPE_F11 = 11
  ROTTYPE_F12 = 12
  ROTTYPE_F13 = 13
  ROTTYPE_RAND = 14
  ROTTYPE_RANDFH = 15
  ROTTYPE_RANDBH = 16
  ROTTYPE_R4 = 17
  ROTTYPE_R6 = 18
  ROTTYPE_INV = 19
  ROTTYPE_FILLER = 20
  ROTTYPE_B1 = 21
  ROTTYPE_B2 = 22
  ROTTYPE_B3 = 23
  ROTTYPE_B4 = 24
  ROTTYPE_B5 = 25
  ROTTYPE_B6 = 26
  ROTTYPE_B7 = 27
  ROTTYPE_B8 = 28
  ROTTYPE_B9 = 29
  ROTTYPE_B10 = 30
  ROTTYPE_B11 = 31
  ROTTYPE_B12 = 32
  ROTTYPE_B13 = 33
  ROTTYPE_END = 34

# defines from file: servo_rot_elev.h
ONE_POT_BIT_VOLT = 0.01953
ELEV_CALIB_LOW = 20.0
ELEV_CALIB_MED_LOW = 26.0
ELEV_CALIB_MED = 32.0
ELEV_CALIB_MED_HIGH = 38.0
ELEV_CALIB_HIGH = 44.0

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
ELEVATION_ANGLE_BALL_MIN = 5.0
ELEVATION_ANGLE_BALL_MAX = 44.0
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
CUSTOM_DRILL_FILES_PATH = "/home/pi/boomer/this_boomers_data/"
NAME_LINE = 1
DESC_LINE = 2
AUDIO_LINE = 3
COLUMN_TITLES_LINE = 4
BEEP_DRILL_NUMBER_START = 901
BEEP_DRILL_NUMBER_END = 979
BEEP_DRILL_LEVEL_NUMBER_START = BEEP_DRILL_NUMBER_START
BEEP_DRILL_LEVEL_NUMBER_END = 929
CUSTOM_DRILL_NUMBER_START = 400
CUSTOM_DRILL_NUMBER_END = 499
THROWER_CALIB_DRILL_NUMBER_START = 760

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
  GPIO_ACCESS_ERROR = 20
  ADC_ERROR_ON_INITIALIZATION = 21
  ADC_EXCESSIVE_READ_ERRORS = 22
  TACH_ERROR_ON_INITIALIZATION = 23
  TACH_EXCESSIVE_READ_ERRORS = 24
  BALL_SWITCH_STUCK_DOWN = 25
  BOTTOM_WHEEL_FAILED_TO_REACH_SPEED = 26
  TOP_WHEEL_FAILED_TO_REACH_SPEED = 27
  LEFT_RIGHT_FAILED_TO_REACH_TARGET = 28
  UP_DOWN_SERVO_FAILED_TO_REACH_TARGET = 29
  CONTROL_PROGRAM_NOT_RUNNING = 30
  CONTROL_PROGRAM_GET_STATUS_FAILED = 31
  CONTROL_PROGRAM_FAILED = 32
  NOT_TRACKING_BALL = 33
  READ_CAMERA_CONFIG_FILE_ERROR = 34
  CAMERA_VECTOR_GENERATION_FAILED = 35
  SETTING_CAMERA_EXPOSURE_FAILED = 36
  CAMERA_FOCAL_LENGTH_CALC_FAILED = 37
  READ_CONFIG_FILE_ERROR = 38
  NOT_PAIRED = 39
  NOT_CONNECTED = 40
  MOTOR_DRIVER_ERROR_ON_INITIALIZATION = 41
  MOTOR_DRIVER_EXCESSIVE_READ_ERRORS = 42
  MOTOR_CALIBRATION_FAILED = 43
  MOTOR_CONFIG_FILE_ERROR = 44
  MOTOR_NOT_DETECTED = 45
  FAULT_END = 46
class net_device_e(Enum):
  LEFT = 0
  RIGHT = 1
  SPEAKER = 2
  BASE = 3
  TRACKING = 4
  UNRECOGNIZED_DEVICE = 5

# defines from file: drill_score.h
class score_method_e(Enum):
  NOT_SCORED = 0
  GROUND = 1
  VOLLEY = 2
  OVERHEAD = 3
  LOB = 4
  DROP = 5
  SERVE_DEUCE = 6
  SERVE_AD = 7
  SERVE_DEUCE_WIDE = 8
  SERVE_DEUCE_T = 9
  SERVE_AD_WIDE = 10
  SERVE_AD_T = 11
  DEUCE = 12
  AD = 13
  SHORT = 14
  DEEP = 15
  VERY_DEEP = 16
  DEUCE_SHORT = 17
  AD_SHORT = 18
  DEUCE_DEEP = 19
  AD_DEEP = 20
  DEUCE_VERY_DEEP = 21
  AD_VERY_DEEP = 22
  DEUCE_THIRD = 23
  CENTER_THIRD = 24
  AD_THIRD = 25
  OUT_OF_CENTER = 26
  DEUCE_SHORT_VERY_WIDE = 27
  AD_SHORT_VERY_WIDE = 28
  DEUCE_DEEP_60 = 29
  AD_DEEP_60 = 30
  SCORE_METHOD_END = 31
