from pysofaconventions import * 
from scipy.spatial import Delaunay 
import scipy.signal 
import numpy as np 
import pyaudio 
import wave 
import time 
import pygame 
from UserInterface import Shape
import sys

def calculate_barycentric(position_coordinates, tetra_coords, transform_matrix, index):
    position_diff = position_coordinates - tetra_coords[index, 3]
    return position_diff @ transform_matrix[index]

def spherical_to_cartesian(azimuth_angle, elevation_angle, radius_distance):
    cos_pel = np.cos(elevation_angle)
    return np.array([
        np.sin(azimuth_angle) * cos_pel * radius_distance,
        np.cos(azimuth_angle) * cos_pel * radius_distance,
        np.sin(elevation_angle) * radius_distance
    ])

def update_hrtf_list(hrtf_list, hrtf_response):
    if not np.array_equal(hrtf_list[-1][0], hrtf_response[0]):
        hrtf_list.append(hrtf_response)

def process_audio_data(wave_file_handle, frame_count, data_prepend, overlap_amount):
    data = wave_file_handle.readframes(frame_count)
    data_integers = np.frombuffer(data, dtype=np.int16)
    data_integers = np.concatenate((data_prepend, data_integers))
    data_prepend = data_integers[-overlap_amount:]
    return data_prepend, data_integers

def calculate_barycentric(position_coordinates, tetra_coords, inverse_transform, index):
    barycentric_coords = (position_coordinates - tetra_coords[index, 3]) @ inverse_transform[index]
    g4 = 1 - sum(barycentric_coords)
    barycentric_coords = list(barycentric_coords)  
    barycentric_coords.append(g4)
    
    return barycentric_coords

def apply_convolution(audio_data, hrtf_filter):
    return scipy.signal.fftconvolve(audio_data, hrtf_filter, mode='full')

def interleave_and_convert_to_bytes(left_channel, right_channel, chunk_size):
    if left_channel.size != right_channel.size:
        raise ValueError("Left and right channels must have the same number of samples.")

    binaural = np.empty((left_channel.size + right_channel.size,), dtype=np.int16)
    binaural[0::2] = left_channel
    binaural[1::2] = right_channel

    data = binaural[:chunk_size * 2].tobytes()
    recording.append(data)

    return (data, pyaudio.paContinue)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)

def handle_keydown(event):
    key_name = pygame.key.name(event.key)
    print(key_name)

    if key_name == "1":
        play_audio('audio_files/story1.wav')
    elif key_name == "2":
        play_audio('audio_files/story2.wav')

def play_audio(file_path):
    wave_file_handle = wave.open(file_path, 'rb')
    print(f"Now is_playing: {file_path}")
    # Add code to play the audio_handle file

def calling(input_data, frame_count, time_info, status):
    position_coordinates = spherical_to_cartesian(azimuth_angle, elevation_angle, radius_distance)
    global current_tetrahedron_index
    iteration_index = 0
    while True:
        barycentric_coordinates = calculate_barycentric(position_coordinates, tetrahedral_coordinates, inverse_transform, current_tetrahedron_index)
        barycentric_coordinates = calculate_barycentric(position_coordinates, tetrahedral_coordinates, inverse_transform, current_tetrahedron_index)
        if all(g >= 0 for g in barycentric_coordinates) or iteration_index>=20000:
            break
        current_tetrahedron_index = triangulation_data.neighbors[current_tetrahedron_index][barycentric_coordinates.index(min(barycentric_coordinates))]
        iteration_index+=1
    
    vertex_indices_list = triangulation_data.simplices[current_tetrahedron_index]
    hrtf_response = sum(fir_filters[idx, :, :] * weight for idx, weight in zip(vertex_indices_list, barycentric_coordinates))
    
    global hrtf_list, prepend_data
    if hrtf_list and not np.array_equal(hrtf_list[-1][0], hrtf_response[0]):
        hrtf_list.append(hrtf_response)
    elif not hrtf_list:
        hrtf_list.append(hrtf_response)
        
    data = wave_file_handle.readframes(frame_count)

    data_integers = np.frombuffer(data, dtype=np.int16) if data else np.array([], dtype=np.int16)

    if data_integers.size > 0:
        data_integers = np.concatenate((prepend_data, data_integers))
    else:
        data_integers = prepend_data

    if data_integers.size >= overlapAmount:
        prepend_data = data_integers[-overlapAmount:]
    else:
        prepend_data = data_integers

   
    left_channel_data = apply_convolution(data_integers, hrtf_response[0])
    right_channel_data = apply_convolution(data_integers, hrtf_response[1])

  
    if len(left_channel_data)>0:
        left_channel_data = left_channel_data[overlapAmount:-overlapAmount]
        left_channel_data = left_channel_data.astype(np.int16)
       

        right_channel_data = right_channel_data[overlapAmount:-overlapAmount]
        right_channel_data = right_channel_data.astype(np.int16)
    
    data, flag = interleave_and_convert_to_bytes(left_channel_data, right_channel_data, audio_chunk_size)
    return (data, flag)


pygame.init()
soundPlot = [[],[]] 
hrtf_list = [[0,0]] 
if True:
   
    def setupHRTF():
       
        folderPath = 'resources/THK_FFHRIR/'
        fileNames = [
            'HRIR_L2354',
            'HRIR_L2354'
        ]
       
        sofaFiles = [SOFAFile(folderPath+fileName+'.sofa','r') for fileName in fileNames]

        
        SourcePosition = np.concatenate([sofaFile.getVariableValue('SourcePosition')
            for sofaFile in sofaFiles])
    
  
        SourcePosition[:,:2] *= np.pi/180

     
        cullAmount = 3

        
        meanFreePath = 4*max(SourcePosition[:,2])/np.sqrt(len(SourcePosition)/cullAmount)
        SourcePosition[len(SourcePosition)//2:,2] += meanFreePath

        maxR = max(SourcePosition[:,2])-meanFreePath/2
        
        fir_filters = np.concatenate([sofaFile.getDataIR()
            for sofaFile in sofaFiles])

        az = np.array(SourcePosition[:,0])
        el = np.array(SourcePosition[:,1])
        r = np.array(SourcePosition[:,2]) 

        xs = np.sin(az)*np.cos(el)*r
        ys = np.cos(az)*np.cos(el)*r
        zs = np.sin(el)*r


        points = np.array([xs, ys, zs]).transpose()

        
        SourcePosition = SourcePosition[::cullAmount]
        fir_filters = fir_filters[::cullAmount]
        points = points[::cullAmount]

        triangulation_data = Delaunay(points, qhull_options="QJ Pp")

        tetrahedral_coordinates = points[triangulation_data.simplices] 
        T = np.transpose(np.array((tetrahedral_coordinates[:,0]-tetrahedral_coordinates[:,3],
                    tetrahedral_coordinates[:,1]-tetrahedral_coordinates[:,3],
                    tetrahedral_coordinates[:,2]-tetrahedral_coordinates[:,3])), (1,0,2))

        def fast_inverse(A):
            identity = np.identity(A.shape[2], dtype=A.dtype)
            Ainv = np.zeros_like(A)
            planarCount=0
            for iteration_index in range(A.shape[0]):
                try:
                    Ainv[iteration_index] = np.linalg.solve(A[iteration_index], identity)
                except np.linalg.LinAlgError:
                    planarCount += 1
            return Ainv

        inverse_transform = fast_inverse(T) 
        return(tetrahedral_coordinates, inverse_transform, triangulation_data, fir_filters, maxR)

    tetrahedral_coordinates, inverse_transform, triangulation_data, fir_filters, maxR = setupHRTF()

    

   
    audio_chunk_size = 30

   
    overlapAmount = fir_filters.shape[2]-1
    prepend_data = np.zeros(overlapAmount)

  
    current_tetrahedron_index = 0

    minR = 0.075
    

      
    fp = 'audio_files/story2.wav'
    keys = pygame.key.get_pressed() 
    
    if keys[pygame.K_1]:
        fp = 'audio_files/story1.wav'  
    elif keys[pygame.K_2]:
        fp = 'audio_files/story2.wav'
    elif keys[pygame.K_2]:
        fp = 'audio_files/story2.wav'
    elif keys[pygame.K_2]:
        fp = 'audio_files/story2.wav'

    wave_file_handle = wave.open(fp, 'rb')
    audio_file = pyaudio.PyAudio()
    recording = []

    source_path = []
  
    
    running = True

    azimuth = 0
    elevation = 0
    dist = maxR
    azimuth_angle = azimuth
    elevation_angle = elevation
    radius_distance = dist

    is_playing = False

    audio_handle = audio_file.open(
        format=audio_file.get_format_from_width(wave_file_handle.getsampwidth()),
        channels=2,
        rate=wave_file_handle.getframerate(),
        output=True,
        frames_per_buffer=audio_chunk_size,
        start = False,
        stream_callback=calling)



def start_ui(source_path=[]):
    global azimuth, elevation, dist, azimuth_angle, elevation_angle, radius_distance, is_playing, fp, wave_file_handle, audio_file  

    source_path = source_path
    source_index = 0
    scrub_time = 0
    limit_time = 0
    startTime = 0
    downTime = 0
    pauseStart = 0

    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  

    BG_COLOR = (217, 217, 217) 
    RED = (249, 36, 114) 
    BG_COLOR = (217, 217, 217)   
    RED = (249, 36, 114)         
    BLUE = (0, 0, 255)           
    GREEN = (0, 255, 0)          
    ORANGE = (255, 165, 0)       
    WHITE = (255, 255, 255)      
    PURPLE = (128, 0, 128)       
    LIGHT_GRAY = (180, 180, 180) 


    
    frames_per_second = 120
    clock = pygame.time.Clock()

    pygame.font.init()  

   
    if not pygame.font.get_init():
        print("Pygame font module could not be initialized.")
        sys.exit()  
        

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    while True:
        handle_events()

        window.fill(BG_COLOR)
           
      
        SCREEN_WIDTH = 720
        SCREEN_HEIGHT = 480
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill((255, 255, 255))  
        

        def text_objects(text, font, color):
            textSurface = font.render(text, True, color)
            return textSurface, textSurface.get_rect()

        
        orig_x = int(SCREEN_WIDTH/2)
        orig_y = int(SCREEN_HEIGHT*0.4)
        dispRad = int(SCREEN_HEIGHT/4)
        polar_plot = Shape(orig_x, orig_y, LIGHT_GRAY, dispRad)


        v_spacing = 50
        azThick = 10
        azPlot_r = SCREEN_HEIGHT//10
        azPlot_x = polar_plot.position[0]
        azPlot_y = polar_plot.position[1]+polar_plot.radius+azPlot_r+v_spacing
        azimuth_plot = Shape(polar_plot.position[0], polar_plot.position[1]+polar_plot.radius+azPlot_r+v_spacing, LIGHT_GRAY, azPlot_r)

        elevation_plot = pygame.Rect(int(orig_x*5/3)-2, orig_y-dispRad/2, 4, dispRad)
        radius_plot = pygame.Rect(int(orig_x*5/3-dispRad/2)-2, orig_y+dispRad, dispRad, 4)

      
        polar_cursor = Shape(orig_x, int(orig_y-90/140*dispRad), BLUE, 10)
        azimuth_cursor = Shape(orig_x, azPlot_y-azPlot_r, BLUE, 10)
        elevation_cursor = Shape(elevation_plot.centerx, int(elevation_plot.top+90/140*elevation_plot.height), BLUE, 10)
        radius_cursor = Shape(int(radius_plot.left + (dist-minR)/(maxR-minR)*radius_plot.width), 
                            radius_plot.centery, BLUE, 10)
        cursor_list = [polar_cursor, azimuth_cursor, elevation_cursor, radius_cursor]

        active_cursor = None

        pressing_List = []

        screen_changed = False

        def update_ui():
            window.fill(BG_COLOR)

            if is_playing:
                largeText = pygame.font.SysFont('lucida console',20)
                TextSurf, TextRect = text_objects('EchoTales', largeText, ORANGE)
                TextRect.left = SCREEN_WIDTH/8/2
                TextRect.top = SCREEN_HEIGHT/8/2
                window.blit(TextSurf, TextRect)

               

            if not is_playing:
                padding = 10 

                largeText = pygame.font.SysFont('lucida console', 22)
                TextSurf, TextRect = text_objects('EchoTales (Press 1-4 to listen to stories)', largeText, ORANGE)
                TextRect.left = SCREEN_WIDTH / 8 / 2
                TextRect.top = SCREEN_HEIGHT / 8 / 2
                window.blit(TextSurf, TextRect)

                second_text_top = TextRect.bottom + padding

                largeText = pygame.font.SysFont('lucida console', 18)
                TextSurf, TextRect = text_objects('1.Cindrella Story', largeText, BLUE)
                TextRect.left = SCREEN_WIDTH / 8 / 2
                TextRect.top = second_text_top  
                TextRect.top = second_text_top 
                window.blit(TextSurf, TextRect)

                third_text_top = TextRect.bottom + padding

                largeText = pygame.font.SysFont('lucida console', 18)
                TextSurf, TextRect = text_objects('2.Ant Story', largeText, BLUE)
                TextRect.left = SCREEN_WIDTH / 8 / 2
                TextRect.top = third_text_top  
                TextRect.top = third_text_top 
                window.blit(TextSurf, TextRect)

                fourth_text_top = TextRect.bottom + padding


                largeText = pygame.font.SysFont('lucida console', 18)
                TextSurf, TextRect = text_objects('3.Slow & Steady', largeText, BLUE)
                TextRect.left = SCREEN_WIDTH / 8 / 2
                TextRect.top = fourth_text_top  
                TextRect.top = fourth_text_top 
                window.blit(TextSurf, TextRect)

                fifth_text_top = TextRect.bottom + padding

                largeText = pygame.font.SysFont('lucida console', 18)
                TextSurf, TextRect = text_objects('4.EXIT', largeText, BLUE)
                TextRect.left = SCREEN_WIDTH / 8 / 2
                TextRect.top = fifth_text_top  
                TextRect.top = fifth_text_top 
                window.blit(TextSurf, TextRect)

            polar_plot.draw_ring(window, 5)

            for gradation in [-3, 0, 3, 6]:
                thick = 1
                if gradation == 0:
                    thick = 3
                pygame.draw.circle(
                    window, LIGHT_GRAY,
                    polar_plot.position, int((90-gradation*10)/140*dispRad), thick)

            for gradation in np.linspace(np.pi/2, np.pi*5/2, 9):
                pygame.draw.aaline(
                    window, WHITE,
                    polar_plot.position, (int(polar_plot.position[0]+np.cos(gradation)*polar_plot.radius), 
                    int(polar_plot.position[1]+np.sin(gradation)*polar_plot.radius)))

            polar_cursor.draw_circle(window)

            azimuth_plot.draw_ring(window, azThick)
            azimuth_cursor.draw_circle(window)

            pygame.draw.rect(
                window, LIGHT_GRAY,
                elevation_plot)
            elevation_cursor.draw_circle(window)

            pygame.draw.rect(
                window, LIGHT_GRAY,
                radius_plot)
            radius_cursor.draw_circle(window)

            pygame.display.update()


        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                    
                if not source_path:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            position = pygame.mouse.get_pos()
                            for iteration_index, cursor in enumerate(cursor_list):
                                if ((position[0]-cursor.position[0])**2 + (position[1]-cursor.position[1])**2 < cursor.radius**2):
                       
                                    active_cursor = cursor
                                    mouse_x, mouse_y = event.pos
                                    offset_x = active_cursor.position[0] - mouse_x
                                    offset_y = active_cursor.position[1] - mouse_y
                                    break

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            active_cursor = None

                    elif event.type == pygame.MOUSEMOTION:

                        if active_cursor is not None:
                            mouse_x, mouse_y = event.pos
                            active_cursor.position = (mouse_x + offset_x, mouse_y + offset_y)

                            if active_cursor == polar_cursor:
                                pC_rad = polar_cursor.distance_to(polar_plot)**0.5
                                if pC_rad > polar_plot.radius:
                                    pol_xlim = (polar_cursor.position[0]-polar_plot.position[0])/pC_rad*polar_plot.radius
                                    pol_ylim = (polar_cursor.position[1]-polar_plot.position[1])/pC_rad*polar_plot.radius
                                    polar_cursor.position = (int(pol_xlim)+polar_plot.position[0],
                                                    int(pol_ylim)+polar_plot.position[1])

                            elif active_cursor == azimuth_cursor:
                                aC_rad = azimuth_cursor.distance_to(azimuth_plot)**0.5
                                if aC_rad != azimuth_plot.radius:
                                    az_xlim = (azimuth_cursor.position[0]-azimuth_plot.position[0])/aC_rad*azimuth_plot.radius
                                    az_ylim = (azimuth_cursor.position[1]-azimuth_plot.position[1])/aC_rad*azimuth_plot.radius
                                    azimuth_cursor.position = (int(az_xlim)+azimuth_plot.position[0],
                                                    int(az_ylim)+azimuth_plot.position[1])

                            elif active_cursor == elevation_cursor:
                                elevation_cursor.position = (elevation_plot.centerx, elevation_cursor.position[1])
                                if elevation_cursor.position[1]>elevation_plot.bottom:
                                    elevation_cursor.position = (elevation_cursor.position[0], elevation_plot.bottom)

                                elif  elevation_cursor.position[1]<elevation_plot.top:
                                    elevation_cursor.position = (elevation_cursor.position[0], elevation_plot.top)

                            elif active_cursor == radius_cursor:
                                radius_cursor.position = (radius_cursor.position[0], radius_plot.centery)
                                if radius_cursor.position[0]>radius_plot.right:
                                    radius_cursor.position = (radius_plot.right, radius_cursor.position[1])
                                elif  radius_cursor.position[0]<radius_plot.left:
                                    radius_cursor.position = (radius_plot.left, radius_cursor.position[1])

                if event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    valid_keys = ["1", "2", "3", "4"]
                    pressing_List.append(key_name)
                    if (key_name == "1"):
                            fp = 'audio_files/story1.wav'  
                    elif (key_name == "2"):
                            fp = 'audio_files/story2.wav'
                    elif (key_name == "3"):
                            fp = 'audio_files/story3.wav'
                    
                    
                    wave_file_handle = wave.open(fp, 'rb')
                    audio_file = pyaudio.PyAudio()
                 

                    if key_name =="4":
                        sys.exit()


                    if key_name in valid_keys:
                        is_playing = not is_playing
                        if is_playing:
                            if startTime == 0:
                                startTime = time.time()
                            if pauseStart != 0:
                                downTime = downTime + (time.time()-pauseStart)
                            audio_handle.start_stream()
                            if not source_path:
                                for cursor in cursor_list:
                                    cursor.color=RED
                            else:
                                for cursor in cursor_list:
                                    cursor.color=GREEN
                        else:
                            pauseStart = time.time()
                            audio_handle.stop_stream()
                            for cursor in cursor_list:
                                cursor.color=BLUE

                elif event.type == pygame.KEYUP:
                    key_name = pygame.key.name(event.key)
                    pressing_List.remove(key_name)


            for key in pressing_List:
                if key == 'd':
                    radius_cursor.position = (int(min(radius_cursor.position[0]+radius_plot.width/100, radius_plot.right)), radius_plot.centery)
                elif key == 'a':
                    radius_cursor.position = (int(max(radius_cursor.position[0]-radius_plot.width/100, radius_plot.left)), radius_plot.centery)
                
            if active_cursor == polar_cursor or screen_changed:
                cartesian_x = polar_cursor.position[0] - polar_plot.position[0]
                cartesian_y = polar_cursor.position[1] - polar_plot.position[1]

                polar_az = np.pi/2-np.arctan2(-cartesian_y, cartesian_x)
                polar_el = 90-np.sqrt(cartesian_x**2 + cartesian_y**2)/dispRad*140

                azimuth_cursor.position = (int(np.cos(polar_az-np.pi/2)*azimuth_plot.radius)+azimuth_plot.position[0], 
                                int(np.sin(polar_az-np.pi/2)*azimuth_plot.radius)+azimuth_plot.position[1])
                elevation_cursor.position = (elevation_plot.centerx,
                                int(elevation_plot.bottom-(polar_el+50)/140*elevation_plot.height))

            if screen_changed:
                radius_cursor.position = (int((dist-minR)/(maxR-minR)*radius_plot.width + radius_plot.left),
                                radius_plot.centery)
                screen_changed = False


            if not source_path:
                azimuth = np.arctan2(azimuth_cursor.position[1]-azimuth_plot.position[1], 
                                    azimuth_cursor.position[0]-azimuth_plot.position[0])+np.pi/2
                elevation = (elevation_plot.bottom-elevation_cursor.position[1])/elevation_plot.height*140-50
                elevation = elevation*np.pi/180
                dist = (radius_cursor.position[0]-radius_plot.left)/radius_plot.width*(maxR-minR) + minR
            else:
                if is_playing:
                    scrub_time = time.time()-startTime-downTime
                if scrub_time >= limit_time:
                    if source_index >= len(source_path):
                        break
                    azimuth = source_path[source_index][0]
                    elevation = source_path[source_index][1]
                    dist = source_path[source_index][2]
                    limit_time = limit_time + source_path[source_index][3]

                    source_index += 1

            azimuth_angle = -azimuth
            elevation_angle = elevation
            radius_distance = dist

            if active_cursor in cursor_list[1:3]:
                polar_cursor.position = (int(np.cos(azimuth-np.pi/2)*polar_plot.radius*(90-elevation*180/np.pi)/140)+polar_plot.position[0], 
                                int(np.sin(azimuth-np.pi/2)*polar_plot.radius*(90-elevation*180/np.pi)/140)+polar_plot.position[1])


            update_ui()
            clock.tick(frames_per_second)

start_ui(source_path)
pygame.quit()
audio_handle.close()
wave_file_handle.close()
audio_file.terminate()