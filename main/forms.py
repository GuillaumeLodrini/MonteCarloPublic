from django import forms
 
# creating a form

#  get_results(d1: Any, d2: Any, m1Base: Any, m1Delta: Any, m2Base: Any,
        #  m2Delta: Any, theta1Base: Any, theta1Delta: Any, theta2Base: Any,
        #  theta2Delta: Any, theta1fBase: Any, theta1fDelta: Any, theta2fBase: Any,
        #  theta2fDelta: Any, n: Any, a1Base: Any, a1Delta: Any, a2Base: Any, a2Delta: Any) -> tuple[Figure, Figure, Figure]
class InputForm(forms.Form):
    # Vehicle 1
    d1 = forms.FloatField(label='Distance to Final Position')

    m1Base = forms.FloatField(label='Mass Base')
    m1Delta = forms.FloatField(label='Mass Delta')

    theta1Base = forms.FloatField(label='Pre-Impact Angle Base')
    theta1Delta = forms.FloatField(label='Pre-Impact Angle Delta')

    theta1fBase = forms.FloatField(label='Post-Impact Angle Base')
    theta1fDelta = forms.FloatField(label='Post-Impact Angle Delta')

    a1Base = forms.FloatField(label='Deceleration Base')
    a1Delta = forms.FloatField(label='Deceleration Delta')

    # Vehicle 2
    d2 = forms.FloatField(label='Distance to Final Position')

    m2Base = forms.FloatField(label='Mass Base')
    m2Delta = forms.FloatField(label='Mass Delta')

    theta2Base = forms.FloatField(label='Pre-Impact Angle Base')
    theta2Delta = forms.FloatField(label='Pre-Impact Angle Delta')

    theta2fBase = forms.FloatField(label='Post-Impact Angle Base')
    theta2fDelta = forms.FloatField(label='Post-Impact Angle Delta')

    a2Base = forms.FloatField(label='Deceleration Base')
    a2Delta = forms.FloatField(label='Deceleration Delta')

