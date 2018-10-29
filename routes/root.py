import subprocess
import timeit

from flask import Blueprint, current_app, flash, render_template, request

from submission.game_submission import FeedbackForm, get_game, load_games

ns = Blueprint('root', __name__)

timer = None
time_elapsed = 0


@ns.route('/')
def index():
	return render_template('routes/home.html', games=load_games())


@ns.route('/game/<title>', methods=['GET', 'POST'])
def show_game(title):
	form = FeedbackForm()
	game = get_game(title)
	global time_elapsed
	global timer

	if not game or not hasattr(game, 'path'):
		return index()

	if request.method == 'POST':

		if not form.validate():
			flash('Rating Required')
			return render_template('routes/post_game.html', game=game, form=form,
			                       timeout=current_app.config['RATE_GAME_IDLE_RESET'])
		else:
			form.output_to_log(game, time_elapsed)
			return show_thanks()

	else:
		timer = timeit.default_timer()
		try:
			process = subprocess.run(game.path, shell=True, timeout=current_app.config['GAME_TIMEOUT_SECONDS'])

		except subprocess.TimeoutExpired:
			pass  # log here user ran out of time

	time_elapsed = timeit.default_timer() - timer

	if not hasattr(game, 'disableReview') or not game.disableReview:

		return render_template('routes/post_game.html', game=game, form=form,
		                       timeout=current_app.config['RATE_GAME_IDLE_RESET'])
	else:
		return show_thanks()


@ns.route('/games')
def show_games():
	return render_template('components/game_list.html', games=load_games())


@ns.route('/thanks')
def show_thanks():
	return render_template('routes/thank_you.html')
