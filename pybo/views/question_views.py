from datetime import datetime
from config import BASE_DIR

from flask import Blueprint, render_template, request, url_for, g
from werkzeug.utils import redirect

from .. import db

from ..models import Question
from ..forms import QuestionForm, AnswerForm

from pybo.views.auth_views import login_required

import os
UPLOAD_DIR = "upload/"

PEOPLE_FOLDER = os.path.join('static', 'upload')


bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)

    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    filename = str(question.user_id) +'_'+ str(question.id) +'_'+str(question.file_upload)
    path =  os.path.join(UPLOAD_DIR, str(question.user_id)+ '_' + str(question.id) + '_' + question.file_upload)
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
    tmpdirectory = os.path.join(BASE_DIR, filename)

    return render_template('question/question_detail.html', question=question, form=form, filename = filename)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    tmpdate = datetime.now()
    tmpfilename = ""
    uploadFlag = False

    if request.method == 'POST' and form.validate_on_submit():

        if request.files['file']:
            tmpfilename = request.files['file'].filename
            uploadFlag = True
            

        question = Question(subject=form.subject.data, content=form.content.data, create_date=tmpdate, user=g.user, file_upload = tmpfilename)
        db.session.add(question)
        db.session.commit()

        if uploadFlag:
            # file upload
            f = request.files['file'] 
            fname = (f.filename) 
            path =  os.path.join(BASE_DIR+"\\pybo\\static\\upload\\", str(question.user_id)+ '_' + str(question.id) + '_' + fname)
            # print(path)
            f.save(path)
        
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    # filename = str(question.user_id) +'_'+ str(question.id) +'_'+str(question.file_upload)
    filename = str(question.file_upload)
    uploadFlag = False

    
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    if request.method == 'POST':
        form = QuestionForm()

            
        if request.files['file']:
            tmpfilename = request.files['file'].filename
            uploadFlag = True


        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            
            if uploadFlag:
            # file upload
                f = request.files['file'] 
                fname = (f.filename) 
                path =  os.path.join(BASE_DIR+"\\pybo\\static\\upload\\", str(question.user_id)+ '_' + str(question.id) + '_' + fname)
                # print(path)
                f.save(path)
                question.file_upload = f.filename       
            else:
                question.file_upload = filename
            
            
            db.session.commit()

            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form, filename = filename)
# --------------------------------------------------------------------------- #


@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))