# myapp/context_processors.py

def student_id(request):
    return {'student_id': request.session.get('selected_study_id', None)}
