def url_to_video(url):
    from pytube import YouTube
    video = YouTube(url)
    audio = video.streams.filter(file_extension='mp4', only_audio=True).first()
    title = "_".join(audio.title[:15].split(' '))
    name = f"{title}.mp4"
    audio.download('static/video/', filename=name)
    return name


def video_to_text(video_name):
    import moviepy.editor as mp
    import speech_recognition as sr

    # Load the video
    video_path = fr"static\video"+fr"\{video_name}"
    # print(video_path)
    audio = mp.AudioFileClip(video_path)
    # Extract the audio from the video
    # audio_file = video.audio
    aud_path = video_path.split('\\')[-1][:-4]
    aud_duration = audio.duration
    audio_path = fr"static\audio\{aud_path}.wav"
    audio.write_audiofile(audio_path)
    # create a speech recognition object
    r = sr.Recognizer()

    # a function to recognize speech in the audio file
    # so that we don't repeat ourselves in in other functions
    def transcribe_audio(path):
        # use the audio file as the audio source
        with sr.AudioFile(path) as source:
            audio_listened = r.record(source)
            # try converting it to text
            text = r.recognize_google(audio_listened)
        return text

    # a function that splits the audio file into chunks on silence
    # and applies speech recognition
    def get_large_audio_transcription_on_silence(path, duration=28):
        import os 
        from pydub import AudioSegment
        # open the audio file using pydub
        sound = AudioSegment.from_file(path)
        if duration<20:
            chunk_length_ms = int(1000 * 60 * 0.05) # convert to milliseconds
        else:
            chunk_length_ms = int(1000 * 60 * 0.20) # convert to milliseconds
        chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
        folder_name = fr"static\audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            try:
                text = transcribe_audio(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += text
        # return the text for all chunks detected
        return whole_text
    text = get_large_audio_transcription_on_silence(audio_path, aud_duration)
    return text


def text_to_summary(text):
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    # Tokenizing the text
    try:
        stopWords = set(stopwords.words("english"))
    except:
        nltk.download('stopwords')
        nltk.download('punkt')
        stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    # Creating a frequency table to keep the
    # score of each word
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    # Creating a dictionary to keep the score
    # of each sentence
    sentences = sent_tokenize(text)
    if len(sentences)<2:
        summary = sentences[0] if sentences else "Video doesn't have audio"
    else:
        sentenceValue = dict()
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]
        # Average value of a sentence from the original text
        average = int(sumValues / len(sentenceValue))
        # Storing sentences into our summary.
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
    return summary


def get_summary(file=None, url=None):
    if file:
        file_name = file.split('/')[-1]
        text = video_to_text(file_name)
        summary = text_to_summary(text)
    else:
        file_name = url_to_video(url)
        text = video_to_text(file_name)
        summary = text_to_summary(text)
    return summary