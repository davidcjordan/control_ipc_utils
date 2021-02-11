# control IPC testing

ctrl_messaging_routines contain the primitives to send GET/PUT messages

make_defines parses .h files to generate the control_ipc_defines.py file so that c language defines can be used by the python scripts and web-UI

scripts to control boomer:
- calib:
    - if called with no args, will get the camera calibration points
    - the 2nd arg specifies the camera ID
    - if called with -- arguments, e.g. --nblx for Near Baseline Left X, will PUT just those points
    - if called witout -- args, the calib points a positional - have to populate at least 10 X and 10 Y points
    - examples:  
         `calib`  
         `calib 1`  
         `./calib 1 --nblx 12.3 --nbly 45.6 --nbrx 78.9 --nbry 20.2`  
         `/calib 0 100.1 200.1 100.1 1000.1 100.1 1500.1 500.2 200.2 1000.2 500.2 1500.2 500.2 700.3 200.3 700.3 500.3 700.3 1500.3 900.4 200.4`

- game: starts a game; args are -l level and -t tiebreaker - but use game -h to get a list of args.
- drill: starts a drill; besides level, args are -i for drill num, -s speed, -H height, -d delay - but use game -h to get a list of args.
- stop: sends stop command and will stop the drill or game
- pause:
- resume



