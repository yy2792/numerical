Interpolation
===

Index
---
<!-- TOC -->
- [Error in Polynomial Interpolation](#Error-in-Polynomial-Interpolation)
- [Cubic Spline](#Cubic-Spline)
<!-- /TOC -->

## Error in Polynomial Interpolation

[Reference STBU 2.1.4]()


[f1]: http://chart.apis.google.com/chart?cht=tx&chl=m=\frac{m_0}{\sqrt{1-{\frac{v^2}{c^2}}}}
[f2]: http://chart.apis.google.com/chart?cht=tx&chl=E_k=mc^2-m_0c^2
[f3]: http://chart.apis.google.com/chart?cht=tx&chl=E=mc^2
[f4]: http://chart.apis.google.com/chart?cht=tx&chl=m_0c^2

## Cubic Spline

### Exists?

![f_c1]

Given ![f_c8], 4n unkonwn

- ![f_c2]<br>
- ![f_c3]<br>
- ![f_c4]<br>
- ![f_c5]<br>

[f_c1]:http://chart.apis.google.com/chart?cht=tx&chl=P_i(x)=a_ix^3%2Bb_ix^2%2Bc_ix%2Bd_i
[f_c2]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}(x_{i-1})=y_{i-1}
[f_c3]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}(x_{i})=y_{i}
[f_c4]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}'(x_{i})=P_i'(x_{i})
[f_c5]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}''(x_{i})=P_i''(x_{i})
[f_c8]:http://chart.apis.google.com/chart?cht=tx&chl=(x_0,y_0),(x_1,y_1),\dots,(x_n,y_n)

We have n, n, n-1, n-1, in all 4n-2 equations with 2 degrees freedom

Common constraints:

- A. Natural Spline:<br>
![f_c6]<br>
- B. Periodic:<br>
![f_c7]<br>
k = 0, 1, 2
- C. First Derivative Assignment:<br>
![f_c9]<br>
![f_c10]<br>

[f_c6]:http://chart.apis.google.com/chart?cht=tx&chl=S''_{\Delta}(a)=S''_{\Delta}(b)=0
[f_c7]:http://chart.apis.google.com/chart?cht=tx&chl=S^{k}_{\Delta}(a)=S^{k}_(b)
[f_c9]:http://chart.apis.google.com/chart?cht=tx&chl=S'_{\Delta}(a)=y_0'
[f_c10]:http://chart.apis.google.com/chart?cht=tx&chl=S'_{\Delta}(b)=y_n'

### Why Cubic?

- **Thm:**<br> 
Let ![w_1]<br>
suppose f is sufficiently nice (see STBU), then<br>
![w_2]<br>
**I** = ![I_form](images/I_form.jpg)

[w_1]:http://chart.apis.google.com/chart?cht=tx&chl={||f||}^2=\int_{a}^{b}{||f''(x)||}^2dx
[w_2]:http://chart.apis.google.com/chart?cht=tx&chl={||f-S_{\Delta}||}^2={{||f||}^2-{||S_{\Delta}||}^2-2I}

[Reference STBU 2.4.1.4]()

- **Thm:**<br>
A or B or C constraint above holds, ![w_4]<br>
Minimum Curvature Property

![I_form2](images/I_form2.jpg)

- ![w_5]

[w_3]:http://chart.apis.google.com/chart?cht=tx&chl={||f||}^2=\int_{a}^{b}{||f''(x)||}^2dx
[w_4]:http://chart.apis.google.com/chart?cht=tx&chl=I=0
[w_5]:http://chart.apis.google.com/chart?cht=tx&chl=f(x_i)=S_{\Delta}(x_i)

[Reference STBU 2.4.1.5]()
