# Implementation Plan - Fix Bot Verbosity & Audio

## Goal
1.  **Reduce Yapping**: Stop the bot from hallucinating detailed explanations about names/inputs during translation.
2.  **Fix Audio**: Ensure the text-to-speech audio plays correctly in the frontend.

## User Review Required
> [!IMPORTANT]
> I am removing the "empathetic" instruction from the translation prompt to prevent the bot from adding unnecessary commentary. This will make the bot more direct.

## Proposed Changes

### [Translation Service]
#### [MODIFY] [app/services/translation_service.py](file:///d:/Insurance%20Agent/app/services/translation_service.py)
- Update `translate_to_user_lang` prompt:
    - Remove "Keep the tone professional, polite, and empathetic".
    - Add explicit instruction: "Do NOT add any explanations, extra context, or definitions. Translate ONLY the provided text."

### [Audio Service / Agent]
#### [MODIFY] [app/services/agent_service.py](file:///d:/Insurance%20Agent/app/services/agent_service.py)
- Add logging to confirm `audio_url` generation.
- Ensure the URL construction handles both `localhost` and `127.0.0.1` (though `localhost` is standard).
- Verify `tts_enabled` logic path.

### [Frontend]
#### [MODIFY] [frontend/src/components/Message.jsx](file:///d:/Insurance%20Agent/frontend/src/components/Message.jsx)
- Check `<audio>` tag attributes. Ensure `preload="metadata"` is set to allow duration loading.

## Verification Plan

### Manual Verification
1.  **Translation Test**:
    - Input: "My name is Harshal Andhale" (in Hindi/Marathi mode).
    - Expected Output: Simple translation of the acknowledgment. NO paragraph about name meaning.
2.  **Audio Test**:
    - Enable Voice in Settings.
    - Send a message.
    - Verify `audio_url` in browser network tab (F12).
    - Check if file exists in `d:/Insurance Agent/app/static/voice_cache`.
    - Verify audio plays.
