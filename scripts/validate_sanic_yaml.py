import yaml
import subprocess
import os

from unittest import TestCase

def valid_sanic_script(script, all_scripts):
  script_words = script.split()
  # TODO: more
  for i, v in enumerate(script_words):
    if v == 'kubectl':
      assert 'sanic' in script_words[i-1]
    if v == 'run' and i and 'sanic' in script_words[i-1]:
      assert script_words[i+1].strip('${}();.,"\'') in all_scripts
  return True

def valid_script(script, all_scripts):
  assert valid_sanic_script(script, all_scripts)

  with open('/tmp/shellcheck', 'w') as f:
    f.write(script)
  # see https://github.com/koalaman/shellcheck/wiki/Ignore
  result = subprocess.check_output([
    'shellcheck', '-s', 'bash', '/tmp/shellcheck', '-e', 'SC2086,SC2155,SC2046',
  ])

  return True

class ValidateSanicYaml(TestCase):
  with open('./sanic.yaml', 'r') as stream:
    config = yaml.load(stream)
    buildables = config['buildables']
    global_scripts = config['scripts']
    environments = config['environments']

  def test_description_given(self):
    for buildable in self.buildables:
      assert self.buildables[buildable]['description']

  def test_correct_build_groups(self):
    for buildable in self.buildables:
      for build_group in self.buildables[buildable].get('build_groups', []):
        assert build_group in self.environments

  def test_folders_exist(self):
    dependencies = set()
    for path in self.buildables:
      assert os.path.isfile(os.path.join('.', path, 'Dockerfile'))
      dependencies = dependencies.union(set(self.buildables[path].get('build_dependencies', [])))
    for dependency in dependencies:
      assert os.path.isfile(os.path.join('.', dependency, 'factory.Dockerfile'))

  def test_valid_global_scripts(self):
    for script in self.global_scripts:
      assert valid_script(self.global_scripts[script], self.global_scripts)

  def test_valid_env_scripts(self):
    for environment in self.environments:
      scripts = self.environments[environment].get('scripts', [])
      all_scripts = set(self.global_scripts).union(set(scripts))
      for script in scripts:
        assert valid_script(scripts[script], all_scripts)


