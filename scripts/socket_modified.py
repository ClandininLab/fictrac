#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 33334         # The port used by the server

# Open the connection (FicTrac must be waiting for socket connection)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    # Keep receiving data until FicTrac closes
    while True:
        # Receive one data frame
        data = sock.recv(1024)
        if not data:
            break

        # Decode received data
        line = data.decode('UTF-8')
        endline = line.find("\n")
        line = line[:endline]
        toks = line.split(", ")

        # Fixme: sometimes we read more than one line at a time,
        # should handle that rather than just dropping extra data...
        if ((len(toks) < 24) | (toks[0] != "FT")):
            print('Bad read')
            continue

        # Extract FicTrac variables
        # (see https://github.com/rjdmoore/fictrac/blob/master/doc/data_header.txt for descriptions)
        cnt = int(toks[1])
        dr_cam = [float(toks[2]), float(toks[3]), float(toks[4])]
        err = float(toks[5])
        dr_lab = [float(toks[6]), float(toks[7]), float(toks[8])]
        r_cam = [float(toks[9]), float(toks[10]), float(toks[11])]
        r_lab = [float(toks[12]), float(toks[13]), float(toks[14])]
        posx = float(toks[15])
        posy = float(toks[16])
        heading = float(toks[17])
        step_dir = float(toks[18])
        step_mag = float(toks[19])
        intx = float(toks[20])
        inty = float(toks[21])
        ts = float(toks[22])
        seq = int(toks[23])
        #sync = int(toks[24])
        sync = toks[24]

        # Do something ...
        print(f'posx: {posx}, posy: {posy}, sync: {sync}')

    # COL     PARAMETER                       DESCRIPTION
    # 1       frame counter                   Corresponding video frame (starts at #1).
    # 2-4     delta rotation vector (cam)     Change in orientation since last frame,
    #                                         represented as rotation angle/axis (radians)
    #                                         in camera coordinates (x right, y down, z
    #                                         forward).
    # 5       delta rotation error score      Error score associated with rotation
    #                                         estimate.
    # 6-8     delta rotation vector (lab)     Change in orientation since last frame,
    #                                         represented as rotation angle/axis (radians)
    #                                         in laboratory coordinates (see
    #                                         *configImg.jpg).
    # 9-11    absolute rotation vector (cam)  Absolute orientation of the sphere
    #                                         represented as rotation angle/axis (radians)
    #                                         in camera coordinates.
    # 12-14   absolute rotation vector (lab)  Absolute orientation of the sphere
    #                                         represented as rotation angle/axis (radians)
    #                                         in laboratory coordinates.
    # 15-16   integrated x/y position (lab)   Integrated x/y position (radians) in
    #                                         laboratory coordinates. Scale by sphere
    #                                         radius for true position.
    # 17      integrated animal heading (lab) Integrated heading orientation (radians) of
    #                                         the animal in laboratory coordinates. This
    #                                         is the direction the animal is facing.
    # 18      animal movement direction (lab) Instantaneous running direction (radians) of
    #                                         the animal in laboratory coordinates. This is
    #                                         the direction the animal is moving in the lab
    #                                         frame (add to animal heading to get direction
    #                                         in world).
    # 19      animal movement speed           Instantaneous running speed (radians/frame)
    #                                         of the animal. Scale by sphere radius for
    #                                         true speed.
    # 20-21   integrated forward/side motion  Integrated x/y position (radians) of the
    #                                         sphere in laboratory coordinates neglecting
    #                                         heading. Equivalent to the output from two
    #                                         optic mice.
    # 22      timestamp                       Either position in video file (ms) or real
    #                                         capture time for image frame.
    # 23      sequence counter                Position in current frame sequence. Usually
    #                                         corresponds directly to frame counter, but
    #                                         can reset to 1 if tracking is reset.
