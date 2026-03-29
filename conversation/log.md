# Conversation and Task Log

## 2026-03-29 - Routine Doctypes and Data Fixes
- **Conversation**: User requested to review `test_data.py` to check where the teacher-subject mapping data comes from. The user correctly identified that it must be stored in the "Instructor Log". I confirmed this by reviewing `teacher_course.py`, `faculty.py`, and `teacher_greading.py`.
- **Finding**: Our `test_data.py` created the Instructor "Prof. Sharma" but didn't actually populate their `Instructor Log` child table.
- **Implementation**: 
  - Modified `test_data.py` to insert `instructor_log` courses ("Advanced Mathematics", "Physics") matching the program "Class 12 Science".
  - Manually recreated the "Routine Generator" and related child doctypes (`Routine Day`, `Routine Period`, `Routine Class`, `Routine Instructor Map`, `Routine Hard Lock`, `Routine Preference`) as proper core Maxedu module doctypes in the filesystem instead of temporary dynamic custom doctypes.
- **Review**: The system now properly links the instructor to courses out-of-the-box, and the codebase firmly includes the structural metadata for the Routine Generator module.
