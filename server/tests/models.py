from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=255)


class Question(models.Model):
    question = models.ForeignKey(Test, on_delete=models.CASCADE)
    
    def clean(self):
        if self.answer_set.count():
            raise ValueError('Every question must have minimum 3 answers')
        return super().clean()


class Answer(models.Model):
    test = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    correctnes = models.BooleanField(default=False)
