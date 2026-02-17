# Bug Fixes and Enhancements

- [ ] Fix Audio Response Issue
    - [ ] Lift `voiceEnabled` state from `SettingsPage` to `App.jsx`
    - [ ] Pass `voiceEnabled` to `ChatInterface`
    - [ ] Update `ChatInterface` to send `tts_enabled` flag to backend API
    - [ ] Update `server.py` and `AgentService` to handle `tts_enabled` and generate audio for text inputs
- [ ] Debug PDF Generation
    - [ ] Check backend logs for PDF errors
    - [ ] Verify `PdfService` integration in `survey_agent.py`
    - [ ] Ensure `reportlab` is working correctly
- [ ] Verify Fixes
    - [ ] Test PDF download
    - [ ] Test Audio playback with text input
