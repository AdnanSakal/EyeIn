import cv2
import mediapipe as mp
from morse_code import morse_code
import time
from sug import search,all_word
from model import prediction
import pyttsx3
def whole():
    engine = pyttsx3.init()


    def speak(text):
        engine.say(text)
        engine.runAndWait()

    to_new_frame_value_sug_r = 0
    cnv_morse_to_word = 0

    left_eye_closed = 0

    pred = ""
    next_word = ""
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    mp_face_mash = mp.solutions.face_mesh
    face_mash = mp_face_mash.FaceMesh(refine_landmarks = True)
    LEFT_IRIS = [468, 469, 470, 471]


    right_eye_close_number = 0
    for_auto_com_data = ""
    sug_word = ""


    #countdown 
    countdown_time = 2
    last_capture_time = time.time()
    countdown_start_time = None
    capturing_frame = False

    #storing data
    binary_data = []
    value_1_if_10 = 0
    morse_data = []



    show_alternate_window = False
    alternate_window_open = False  # Flag to track if alternate window is open





    both_eye_close_time_value = None




    final_auto_com = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        face_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = face_mash.process(face_rgb)
        if result.multi_face_landmarks:
            face_landmarks = result.multi_face_landmarks[0]
            
        

            # for iris go up and down 
            left_eye_top = face_landmarks.landmark[159].y * frame.shape[0]
            left_eye_bottom = face_landmarks.landmark[145].y * frame.shape[0]
            eye_center_y = (left_eye_top + left_eye_bottom) // 2

            # to check if eye is open or closed
            left_eye_height = abs(left_eye_bottom - left_eye_top)

    
            # for closing with right eye
            right_eye_top = face_landmarks.landmark[386].y * frame.shape[0]
            right_eye_bottom = face_landmarks.landmark[374].y * frame.shape[0]
            right_eye_height = abs(right_eye_bottom - right_eye_top)
            


        
    # FOR REMOVING FINAL OUTPUT(LAST WORD FROM SENTENCE)
            if right_eye_height < 15 and left_eye_height < 15:
                to_new_frame_value_sug_r = 0 # 0 na dile chok blink korle etao barbe 
                cnv_morse_to_word = 0
                print("closed")
                if both_eye_close_time_value is None:
                    both_eye_close_time_value = time.time()

                elapsed_time = time.time() - both_eye_close_time_value

                if elapsed_time >= 2:
                    speak("open")
                    final_auto_com = []
            else:
                both_eye_close_time_value = None
                









            #for chnaging window
            if left_eye_height < 15:
                to_new_frame_value_sug_r += 1
                if to_new_frame_value_sug_r == 20:
                    show_alternate_window = True
            else:
                to_new_frame_value_sug_r = 0



    # NEW FRAME ----------------------------------------- 
            if show_alternate_window:
            
                alt_frame = frame.copy()
                binary_data = []
                value_1_if_10 = 0
                cnv_morse_to_word = 0
                morse_data = []
                capturing_frame = False
            
                

                #Text Suggetion --------------------------
                sug = search(all_word,for_auto_com_data.lower())
                if len(sug) >= 5 or len(sug)<=5: # koto gulo suggestion nibo
                    sug = sug[:5]


                    sug.insert(0,"") # we can use this as a 'space' when writing 
                    for i,l in enumerate(sug):
                        x = 450
                        y = 100
                        h = 30
                        cv2.putText(alt_frame,f"{i*10} : {l}",(x,y+i * h),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

                    # TEXT SUG END HERE -----------------------------------------------------------------



                    #FOR CONFERMING SUG WORD AND NEXT WORD -----------------------------

                    if right_eye_height < 15:
                        right_eye_close_number += 1

                
                    cv2.putText(alt_frame,f"eye_close(L): {right_eye_close_number}",
                                (50,100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
                    
                    if right_eye_close_number == 0 and len(sug) >= 1:
                        sug_word = sug[0] + for_auto_com_data.lower()
                    if right_eye_close_number == 10 and len(sug) >= 2:
                        sug_word = sug[1]
                    if right_eye_close_number == 20 and len(sug) >= 3:
                        sug_word = sug[2]
                    if right_eye_close_number == 30 and len(sug) >= 4:
                        sug_word = sug[3]
                    if right_eye_close_number == 40 and len(sug) >= 5:
                        sug_word = sug[4]
                    if right_eye_close_number == 50 and len(sug) >= 6: # chanhge 45 to 50
                        sug_word = sug[5]
    #--------------------------------------------------------

    #--------------------------------------------------------   
    

                elif len(sug) == 0:
                    if right_eye_height < 15:
                        right_eye_close_number += 1
                    cv2.putText(alt_frame,f"eye_close(L): {right_eye_close_number}",
                                (50,100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2) ##########
                    sug_word = for_auto_com_data.lower()


                if right_eye_close_number == 55: # chanhge 50 to 55
                    right_eye_close_number = 0

        
                #FOR PRDICTION IN THE MODEL ------------
                if left_eye_height < 15:
                    left_eye_closed += 1
                    
                if left_eye_closed == 10:
                    next_word = sug_word 
                    pred = prediction(next_word)

            
                #WHAT TO CHOOSE SUGESTED WORD OR NEXT WORD (OR JUST WHAT IN THE MORSE CODE)

                #THIS IS FOR BOTH SUGESTED WORD AND NORMAL OUTPUT 
                if left_eye_closed in range(20,25) and right_eye_close_number in range(20,25):
                    final_auto_com.append(next_word)
                    left_eye_closed = 0
                    show_alternate_window = False

                #THIS IS FOR MODEL PREDICTION CONFIRMATION
                
                if  left_eye_closed in range(40,45) and right_eye_close_number in range(40,45):
                    final_auto_com.append(pred)
                    left_eye_closed = 0
                    show_alternate_window = False
                    


                if left_eye_closed == 55:
                    left_eye_closed = 0



                cv2.putText(alt_frame,f"eye_close(R): {left_eye_closed}",(50,150),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
                
                cv2.putText(alt_frame,f"N: {pred}",(50,200),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
            
                cv2.imshow("Second Frame -> press 'q' to exit", alt_frame)
                if alternate_window_open is False:
                    cv2.destroyWindow("First Frame -> press 'q' to exit")
                    alternate_window_open = True





    # NEW FRAME END HERE -----------------------------------------------------------------------



    # OLD(FIRST FRAME) FRAME START ------------------------------------------------------
            else:
                main_frame = frame.copy()
                
                # converting binary data to morse code
                if right_eye_height < 15:
                    capturing_frame = False
                    cnv_morse_to_word += 1 
                    if cnv_morse_to_word == 5:
                        value_1_if_10 += 1
                    
                    
                        print("eye closed left") 
                
                        if value_1_if_10 > 2 and len(binary_data) >= 1:
                            str_binary = [str(i) for i in binary_data]
                            str_data = "".join(str_binary)
                            try:
                                morse_data.append(morse_code[str_data])
                            except KeyError:
                                morse_data.append("?")
                            binary_data.clear()
                        
                            for_auto_com_data = "".join(morse_data)


                    # for removing new item also reset up_value
                    if cnv_morse_to_word == 20:
                        try:
                            morse_data.pop(-1)
                        except IndexError:
                            pass
                        value_1_if_10 = 0
                else:
                    cnv_morse_to_word = 0

                # CONVERTING MORSE TO WORD CODE "END" HERE --------------------------------------------





                # FOR COUNTING AND LAYOUT OF FRONT FRAME ---------------------------

                if left_eye_height > 15 or left_eye_height < 15:
                    
                    
                    print("eye's is open")
                    
                
                    left_eye_closed = 0
                    right_eye_close_number = 0
                    sug_word = ""
                    if capturing_frame:
                        time_left = countdown_time - int(time.time() - countdown_start_time)
                        if time_left > 0 :
                            cv2.putText(main_frame,str(time_left),(50,50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        else:
                            value = 1 if left_eye_height > 15 else 0
                            binary_data.append(value)
                            # jodi user vul kore 4 er beshi binary data ney tahole amra prothom 4ta data nibo
                            if len(binary_data) > 5:
                                binary_data = binary_data[:5]
                            
                            countdown_start_time = time.time()
                    if time.time() - last_capture_time > 2 and not capturing_frame:
                        countdown_start_time = time.time()
                        capturing_frame = True

                cv2.putText(main_frame,f"sug(R): {to_new_frame_value_sug_r}",(50,100),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
                cv2.putText(main_frame,f"inc_TC(L): {cnv_morse_to_word}",(50,150),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
            
            
                cv2.putText(main_frame,f"data: {binary_data}",(450,50),cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                                    (0, 255, 0), 2)
            
                # looking 'up' nuber for prediction
                cv2.putText(main_frame,f"Total close: {value_1_if_10}",(450,100),cv2.FONT_HERSHEY_SIMPLEX,0.6,
                                        (0,255,0),2)
                        
                # showing the final output(alphabet that was generated using morse code)
                cv2.putText(main_frame,f"result: {''.join(morse_data)}",(450,150),cv2.FONT_HERSHEY_SIMPLEX,0.6,
                            (0,255,0),2)

                sug = search(all_word,for_auto_com_data.lower())
                if len(sug) >5:
                    sug = sug[:5]
                sug.insert(0,"") # we can use this as a 'space' when writing 
                for i,l in enumerate(sug):
                    x = 450
                    y = 200
                    h = 30
                    cv2.putText(main_frame,f"{i*10} : {l}",(x,y+i * h),
                                cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)

    
                cv2.putText(main_frame,f"Text: {final_auto_com}",(50,400),cv2.FONT_HERSHEY_SIMPLEX,0.6,
                            (0,255,0),2)
            
                cv2.imshow("First Frame -> press 'q' to exit", main_frame)
                if alternate_window_open:
                    cv2.destroyWindow("Second Frame -> press 'q' to exit")
                    alternate_window_open = False






        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

