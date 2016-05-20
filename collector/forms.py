from django import forms


class ResultsForm(forms.Form):
    # Parties
    choices_candidates = (
        ('RP', 'Republican Party'),
        ('DP', 'Democratic Party'),
        ('DT', 'Donald Trump'),
        ('HC', 'Hillary Clinton'),
        ('BS', 'Bernie Sanders'),
        ('MR', 'Marco Rubio'),
        ('TC', 'Ted Cruz'),
    )
    choices_dates = (
        ('AA', 'All'),
        ('ST', 'Super Tuesday'),
        ('FP', 'Florida Primaries'),
        ('RD', 'Republican Debate'),
        ('DD', 'Democratic Debate'),
    )
    option = forms.ChoiceField(choices=choices_candidates)
    event = forms.ChoiceField(choices=choices_dates)


class CompareForm(forms.Form):
    # Parties
    options = ["Choice1", "Choice2", "Choice 3"]
    choices_candidates = (
        ('RP', 'Republican Party'),
        ('DP', 'Democratic Party'),
        ('DT', 'Donald Trump'),
        ('HC', 'Hillary Clinton'),
        ('BS', 'Bernie Sanders'),
        ('MR', 'Marco Rubio'),
        ('TC', 'Ted Cruz'),
    )
    choices_dates = (
        ('AA', 'All'),
        ('ST', 'Super Tuesday'),
        ('FP', 'Florida Primaries'),
        ('RD', 'Republican Debate'),
        ('DD', 'Democratic Debate'),
    )
    option1 = forms.ChoiceField(choices=choices_candidates)
    option2 = forms.ChoiceField(choices=choices_candidates)
    event = forms.ChoiceField(choices=choices_dates)
