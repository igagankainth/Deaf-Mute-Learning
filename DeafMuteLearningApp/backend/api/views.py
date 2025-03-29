from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from googletrans import Translator
from .transcribe import transcribe_audio

translator = Translator()

@csrf_exempt
def translate_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        target_lang = request.POST.get('target_lang', '')

        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)

        if target_lang not in ['hi', 'pa']:
            return JsonResponse({'error': 'Invalid target language'}, status=400)

        try:
            translated = translator.translate(text, dest=target_lang)
            return JsonResponse({'translated_text': translated.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def voice_to_text(request):
    if request.method == 'POST':
        print("Received POST request at /api/voice_to_text/")

        if 'audio' not in request.FILES:
            print("Error: No audio file provided")
            return JsonResponse({'error': 'No audio file provided'}, status=400)

        target_lang = request.POST.get('target_lang', '')
        print(f"Received Target Language: {target_lang}")

        if target_lang not in ['hi', 'pa']:
            print("Error: Invalid target language")
            return JsonResponse({'error': 'Invalid target language'}, status=400)

        # ---- STEP 1: Transcribe ----
        audio_file = request.FILES['audio']
        transcribed_text = transcribe_audio(audio_file)
        print(f"Transcribed Text: {transcribed_text}")

        if not transcribed_text or transcribed_text == "Could not understand audio":
            print("Error: Could not transcribe audio")
            return JsonResponse({'error': 'Could not transcribe audio. Try again with clearer input.'}, status=500)

        # ---- STEP 2: Translate ----
        try:
            translated = translator.translate(transcribed_text, dest=target_lang)
            translated_text = translated.text
            print(f"Translated Text: {translated_text}")
        except Exception as e:
            print(f"Error during translation: {str(e)}")
            return JsonResponse({'error': f'Translation error: {str(e)}'}, status=500)

        # ---- STEP 3: Return BOTH ----
        response_data = {
            'original_text': transcribed_text,
            'translated_text': translated_text
        }
        print("Final Response:", response_data)

        return JsonResponse(response_data)

    print("Error: Only POST method allowed")
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
