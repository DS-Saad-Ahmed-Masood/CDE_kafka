import random
import json

class PollResponseAPI:

  survey_questions = [
      {
          'Q': 'How was the Conference overall? (Rate between 1 - 5)',
          'A': ['1', '2', '3', '4', '5']
      },
      {
          'Q': 'How would you rate the keynote speaker? (Rate between Very Bad - Very Good)',
          'A': ['V. Bad', 'Bad', 'Moderate', 'Good', 'V. Good']
      },
      {
          'Q': 'Did you find the breakout sessions informative?',
          'A': ['Yes', 'No']
      }
  ]

  def poll_response_api(self):

      response = {}

      sample_response = []

      answer_id = random.randint(1000,2000)

      response['answer_id'] = answer_id

      for question in self.survey_questions:

          answer_pair  = { question['Q'] : question['A'][random.randint(0, len(question['A']) - 1)] }

          sample_response.append(answer_pair)

      response['answer_array'] = sample_response

      return json.dumps(response,indent=4)