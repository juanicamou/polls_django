import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse 

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):

        """"
        was_published_recently returns False for questions whose pub_date is in the future.        
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='¿Quien es el mejor alumno', pub_date=time )
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        
        """"
        
        was_published_recently returns False for questions whose pub_date is in the future.        
        """
        time = timezone.now()
        future_question = Question(question_text='¿Quien es el mejor alumno', pub_date=time )
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        
        """"
        was_published_recently returns False for questions whose pub_date is in the future.        
        """
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(question_text='¿Quien es el mejor alumno', pub_date=time )
        self.assertIs(future_question.was_published_recently(), False)

def create_question(question_text, days):

    """
    Create a question with the given "question_text", and published the given number of days offset to now (negative for the question in the past, positive for the question that have yet to be published).    
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):

        """"
        If no question exist, an appropiate message is displayed. 
        """
        response = self.client.get(reverse('polls:index')) # request to index and save response 
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_questions_with_future_pub_date(self):

        """
        Questions with future date are not be displayed on the indexpage.        
        """
        create_question('test future question', 30) # future_question
        response = self.client.get(reverse('polls:index'))
        #self.assertNotIn(future_question, response.context['latest_question_list'])
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_questions_with_past_pub_date(self):
        """
        Questions with past date are displayed on the indexpage.        
        """
        past_question = create_question('Future question', -30)
        response = self.client.get(reverse('polls:index'))
        #self.assertNotIn(future_question, response.context['latest_question_list'])
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        past_question = create_question('Past question', -30)
        create_question('Future question', 30) #future_question
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        past_question_1 = create_question('Past question 1', -30)
        past_question_2 = create_question('Past question 2', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_1, past_question_2])

    def test_two_questions_with_future_pub_date(self):

        """
        Questions with future date are not be displayed on the indexpage.  
        """
        create_question('Future question 1', 30)
        create_question('Future question 2', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionDetailViewTest(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error not found.
        """
        future_question = create_question('Future question', 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past display the question's text.
        """
        past_question = create_question('Past question 1', -30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)