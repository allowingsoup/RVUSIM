import streamlit as st
from openai import OpenAI
from pathlib import Path

# Initialize OpenAI client using secrets
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Hardcode the patient case information
PATIENT_CASE = {
    "patient_name": "John Smith",
    "age": 39,
    "chief_complaint": "my feet are numb",
    "vital_signs": {
        "pulse": 92,
        "respiratory_rate": 12,
        "blood_pressure": "158/96",
        "temperature": 99.0,
        "height": "6'0\"",
        "weight": "235 lbs",
        "bmi": 32,
        "waist_circumference": "41 in"
    },
    "hpi": """
    Onset: 4 days ago
    Setting: started spontaneously while watching TV in the recliner, no apparent triggering event
    Location: started in toes b/l, now at ankles b/l
    Duration: constant
    Character/Quality: numbness (lack of feeling), not a tingling sensation and feels different than feet falling asleep, no pain
    Aggravating factors: nothing apparent
    Alleviating factors: nothing, walking around didn't help
    Associated symptoms: weakness of legs started today
    Radiation: NA
    Timing: constant, not worse at any particular time of day
    Severity: annoying
    Priors: no
    Progression: getting worse, seems to be moving up
    Perceived cause: no idea, no trauma, no changes in activity. Worried if this could be a stroke.
    """,
    "pmh": """
    Chronic illnesses: Peptic ulcer disease (PUD)-dx age 29, Hepatitis A 6 weeks ago, chicken pox as a child
    Surgeries: partial gastrectomy due to ulcers, age 34
    Hospitalizations: none other than above surgery
    Injuries: none
    Health Maintenance: Rarely sees a doctor since on the road full time. Not UTD on immunizations, last Tetanus shot he thinks was in high school. Chicken pox as a child. Didn't get Covid shots. Flu shot 3 weeks ago.
    """,
    "medications": """
    Rx: omeprazole 40 mg QD
    OTC: none
    Supp: none
    """,
    "allergies": """
    Rx: PCN - rash
    Food: walnuts- throat swelling
    Environment: none
    """,
    "social_history": """
    Occupation: long haul truck driver X 5 years, away 4-6 days per week. Cargo is groceries.
    Education: Graduated high school, barely, never really liked school.
    Living situation: Married x 15yrs, 3 kids (ages 8, 10, 13), cat, lives in a home they rent that is in good condition. Safe neighborhood. No prior homelessness.
    Diet: Vegetarian since gastrectomy. 2 meals a day and snacks daily while on the road from convenience store offerings. Doesn't necessarily get a lot of vegetables, but avoids eating meat. Still eats cheese and eggs.
    Exercise: <1x/week. Walks ½-1 mile.
    Sleep: 6 hours per night. Struggles to fall asleep, does so with TV on to avoid hearing environmental highway noises while sleeping in his rig. Wakes up tired. Wife speaks up to say he snores and talks in his sleep.
    Tobacco: 12 pack year hx (1PPD), quit 5 years ago, cigarettes only
    Alcohol: 2-3 beers nightly, couple six packs on weekends
    Drugs: never
    Caffeine: Two 24 oz tanks of coffee daily from the convenience store.
    Sexual History: 3 total prior female partners, currently monogamous with wife, no STI hx. No current condom use.
    Exposures: His 13y/o child has mono this wk. Cat Dx'd with Campylobacter last wk,it is an indoor cat and patient is the one who changes out the litter box. No travel outside US. Hobbies - watching sports.
    Personal Beliefs: Some distrust of medical system, he believes doctors report personal information to the government.
    SDOH: Has Cigna health insurance. No financial or transportation barriers to attaining healthcare.
    """,
    "family_history": """
    Mother: age 63, hypothyroid
    Father: age 65, T2DM
    Paternal Grandparents: both were alcoholics, deceased unknown age
    Maternal Grandparents: died of natural causes in their 80s
    Siblings: none
    """,
    "ros": """
    General: + fatigue recently. No fevers, chills, weight changes.
    HEENT: No sore throat, blurred vision, trouble hearing, or difficulty swallowing.
    Resp: No dyspnea or cough.
    GI: +epigastric pain if he misses doses of omeprazole. Diarrhea with recent Hep A, now resolved. Appetite good. No constipation.
    GU: no urinary or fecal incontinence.
    MSK: + weakness in lower legs b/l. No weakness in upper extremities, no joint pain or swelling. No back pain.
    Neuro: See HPI. No numbness elsewhere. Today had to be careful climbing stairs, felt like tripping. No dizziness, just feels unstable. Speech and memory have been okay. Hasn't passed out.
    Derm: No rashes or skin changes.
    Psych: Gets lonely sometimes while on the road and misses his family. No mood changes. No hx of depression or anxiety. No SI or HI.
    """
}

# Initialize session state for page tracking
if 'page' not in st.session_state:
    st.session_state.page = 'about'

# Navigation function
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Page functions
def about_page():
    st.title("About Page")
    if st.button("Start Simulation"):
        go_to_page('door_sheet')

def door_sheet_page():
    st.title("Door Sheet")
    
    st.subheader("Patient Information")
    st.write(f"Age: {PATIENT_CASE['age']} y/o male")
    st.write(f"Chief Complaint: {PATIENT_CASE['chief_complaint']}")
    
    st.subheader("Vital Signs")
    vitals = PATIENT_CASE['vital_signs']
    st.write(f"Pulse: {vitals['pulse']}")
    st.write(f"Respiratory Rate: {vitals['respiratory_rate']}")
    st.write(f"Blood Pressure: {vitals['blood_pressure']}")
    st.write(f"Temperature: {vitals['temperature']}°F")
    st.write(f"Height: {vitals['height']}")
    st.write(f"Weight: {vitals['weight']}")
    st.write(f"BMI: {vitals['bmi']}")
    st.write(f"Waist Circumference: {vitals['waist_circumference']}")
    
    if st.button("Proceed to Patient Interview"):
        go_to_page('patient_interview')

def patient_interview_page():
    st.title("Patient Interview")
    
    # Initialize chat messages if not already in session state
    if 'patient_messages' not in st.session_state:
        st.session_state.patient_messages = []
        system_message = f"""You are a 39-year-old male patient named Rob with the following characteristics:
        {PATIENT_CASE['hpi']}
        Past Medical History: {PATIENT_CASE['pmh']}
        Medications: {PATIENT_CASE['medications']}
        Allergies: {PATIENT_CASE['allergies']}
        Social History: {PATIENT_CASE['social_history']}
        Family History: {PATIENT_CASE['family_history']}
        Review of Systems: {PATIENT_CASE['ros']}
        Respond as if you were really this patient, maintaining consistency with all provided history. 
        Answers should generally be concise. Only give away 1-2 pieces of information at once."""
        st.session_state.patient_messages.append({"role": "system", "content": system_message})

    # Create main container for chat interface
    chat_container = st.container()
    input_container = st.container()
    nav_container = st.container()

    # Display chat history in the first container
    with chat_container:
        for message in st.session_state.patient_messages:
            if message["role"] in ["user", "assistant"]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Get user input in the second container
    with input_container:
        if prompt := st.chat_input("Ask the patient a question:"):
            st.session_state.patient_messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    for response in client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.patient_messages],
                        stream=True,
                    ):
                        if response.choices:
                            chunk = response.choices[0].delta.content or ""
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.patient_messages.append({"role": "assistant", "content": full_response})

    # Add spacing
    st.write("")
    st.write("")

    # Navigation buttons in the third container
    with nav_container:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Door Sheet"):
                go_to_page('door_sheet')
        with col2:
            if st.button("Proceed to Physical Exam"):
                go_to_page('physical_exam')


def load_all_media_files():
    """Load all media files from the media directory."""
    media_files = [
        "SimMedia/HeartSounds.mp3",
        "SimMedia/TandemGait.mp4",
        "SimMedia/Tonsils.jpg"
    ]
    
    # Define allowed extensions for all media types
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif',  # Images
                          '.mp3', '.wav', '.ogg',           # Audio
                          '.mp4', '.mov', '.avi']           # Video
    
    return media_files

def physical_exam_page():
    """Physical Exam Page."""
    st.title("Physical Exam")
    
    # Set up the media directory
    media_dir = "media"  # Ensure this directory exists and contains relevant files
    
    # Load media files
    media_files = load_all_media_files(media_dir)
    if not media_files:
        st.warning("No media files found in the 'media' directory.")
        st.stop()
    
    # Dropdown for selecting a media file
    selected_media = st.selectbox(
        "Select a media file to view/play:",
        media_files,
        format_func=lambda x: Path(x).name  # Display only the file name
    )
    
    # Determine the type of file and display it appropriately
    ext = Path(selected_media).suffix.lower()
    if ext in ['.jpg', '.jpeg', '.png', '.gif']:
        # Display an image
        st.image(
            selected_media,
            caption=Path(selected_media).name,
            use_container_width=True
        )
    elif ext in ['.mp3', '.wav', '.ogg']:
        # Play an audio file
        with open(selected_media, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format=f'audio/{ext[1:]}', start_time=0)
    elif ext in ['.mp4', '.mov', '.avi']:
        # Play a video file
        with open(selected_media, 'rb') as video_file:
            video_bytes = video_file.read()
        st.video(video_bytes, format=f'video/{ext[1:]}')
    else:
        st.error("Unsupported file type.")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Patient Interview"):
            go_to_page('patient_interview')
    with col2:
        if st.button("Proceed to Case Presentation"):
            go_to_page('case_presentation')


def case_presentation_page():
    st.title("Case Presentation")

    st.write("Record yourself giving a case presentation.")
    st.write("Your audio will be transcribed and graded.")

    # Audio Recording Input
    audio_recording = st.audio_input("Record your case presentation", 
                                   key="case_presentation_recording")
    
    if audio_recording:
        st.info("Transcribing your audio...")

        # Transcribe using Whisper-1
        try:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_recording,
                response_format="text"
            )
            
            st.success("Audio transcription completed!")
            st.subheader("Your Transcription:")
            st.write(transcription)
        
        except Exception as e:
            st.error(f"An error occurred during transcription: {e}")
            return

        # Grade the transcript with GPT-4o-mini
        st.info("Grading your case presentation...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful and professional attending physician."},
                    {"role": "user", "content": f"Please grade this medical student case presentation and provide constructive feedback. Consider clarity, structure, and thoroughness in your evaluation:\n\n{transcription}"}
                ]
            )
            
            feedback = response.choices[0].message.content
            st.success("Grading Complete!")
            st.subheader("Feedback from the Attending:")
            st.write(feedback)

        except Exception as e:
            st.error(f"An error occurred while grading the presentation: {e}")
            return

        # Display the recording
        st.subheader("Your Recording:")
        st.audio(audio_recording)

    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Physical Exam"):
            go_to_page('physical_exam')
    with col2:
        if st.button("Proceed to Debrief"):
            go_to_page('debrief')

def debrief_page():
    st.title("Debrief Session")
    
    st.write("This is your opportunity to discuss your assessment and plan for this patient case.")
    
    # Assessment Section
    st.subheader("Assessment")
    assessment = st.text_area(
        "What is your assessment of this patient? Consider differential diagnoses and their likelihood.",
        height=200,
        placeholder="Enter your assessment here..."
    )

    # Plan Section
    st.subheader("Plan")
    plan = st.text_area(
        "What is your proposed plan for this patient? Include diagnostics, treatments, and follow-up.",
        height=200,
        placeholder="Enter your plan here..."
    )

    # Submit button for feedback
    if st.button("Submit for Feedback"):
        if assessment and plan:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an experienced attending physician providing feedback on a medical student's assessment and plan."},
                        {"role": "user", "content": f"""
                        Please evaluate this medical student's assessment and plan for our patient with bilateral foot numbness.
                        
                        Student's Assessment:
                        {assessment}
                        
                        Student's Plan:
                        {plan}
                        
                        Provide specific, constructive feedback on:
                        1. Strengths of their assessment and plan
                        2. Areas for improvement
                        3. Key points they may have missed
                        """}
                    ]
                )
                
                st.success("Feedback received!")
                st.subheader("Attending's Feedback:")
                st.write(response.choices[0].message.content)
            
            except Exception as e:
                st.error(f"An error occurred while getting feedback: {e}")
        else:
            st.warning("Please complete both the assessment and plan before submitting.")

    # Navigation
    if st.button("Finish Simulation"):
        go_to_page('thank_you')

def thank_you_page():
    st.title("Thank You!")
    st.write("Thank you for completing the medical simulation!")
    if st.button("Start New Simulation"):
        go_to_page('about')

# Main app logic
def main():
    if st.session_state.page == 'about':
        about_page()
    elif st.session_state.page == 'door_sheet':
        door_sheet_page()
    elif st.session_state.page == 'patient_interview':
        patient_interview_page()
    elif st.session_state.page == 'physical_exam':
        physical_exam_page()
    elif st.session_state.page == 'case_presentation':
        case_presentation_page()
    elif st.session_state.page == 'debrief':
        debrief_page()
    elif st.session_state.page == 'thank_you':
        thank_you_page()

if __name__ == "__main__":
    main()
