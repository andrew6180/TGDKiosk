import datetime
import os
import time
from enum import Enum

from flask import render_template
from flask_wtf import FlaskForm
from ruamel.yaml import YAML, yaml_object
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import InputRequired
from wtforms.widgets import HiddenInput

yaml = YAML()

games = []


@yaml_object(yaml)
class Game(object):
	def __init__(self):
		self.title = ""
		self.author = ""
		self.summary = ""
		self.group = Group.TGD
		self.banner = "http://placehold.it/1440x300"
		self.path = ''

	def dump_yaml(self):
		if not self.author or not self.title:
			raise ValueError('Author or Title is empty')

		file_name = os.path.join(Game.get_data_path(), f'{self.author}_{self.title}\\data.yaml')
		os.makedirs(os.path.dirname(file_name), exist_ok=True)

		with open(file_name, 'w') as file:
			yaml.dump(self, file)

	@staticmethod
	def get_data_path():
		return os.path.join(os.getcwd(), 'static', f'game_configs/')


@yaml_object(yaml)
class Group(Enum):
	TGD = 1
	PIMA = 2
	UOFA = 3

	@classmethod
	def to_yaml(cls, representer, node):
		return representer.represent_scalar(
			u'!Group',
			f'{node.name}'
		)

	@classmethod
	def from_yaml(cls, constructor, node):
		return Group[node.value]


def load_games():
	global games
	games = []
	for root, dirs, files in os.walk(Game.get_data_path()):
		for file_name in files:
			if file_name.endswith('.yaml'):
				with open(os.path.join(root, file_name), 'r') as file:
					try:
						game = yaml.load(file)
						game.path = os.path.join('static', game.path)
						game.banner = os.path.join('static', game.banner)
						games.append(game)
					except Exception as ex:
						print(ex)
	return games


def get_game(title):
	if not games:
		load_games()

	for game in games:
		if game.title == title:
			return game

	return None


class FeedbackForm(FlaskForm):
	rating = IntegerField(widget=HiddenInput(), validators=[InputRequired()])
	feedback = TextAreaField('Feedback')
	name = StringField('Name or Contact:')

	def output_to_log(self, game, time_played):
		print(self.name.data)
		if not self.name.data:
			self.name.data = "Anonymous"

		path = os.path.join(os.getcwd(), "feedback", f'{game.author}_{game.title}\\')

		path_exists = os.path.exists(path)

		if not path_exists:
			os.makedirs(path)
		file_path = os.path.join(path, 'feedback.html')
		file_exists = os.path.isfile(file_path)

		with open(file_path, 'a+') as file:
			if not file_exists:
				file.write(render_template('components/rating_result_boilerplate.html', game=game))

			date_time = datetime.datetime.now()
			date_time = date_time.strftime("%a, %m/%d @ %I:%M:%S %p")

			time_played_raw = time_played
			time_played = time.strftime("%M:%S", time.gmtime(time_played))

			file.write(
				render_template('components/rating_result.html', form=self, datetime=date_time,
				                time_played=time_played, time_played_raw=time_played_raw))
			file.close()
