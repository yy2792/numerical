Interpolation
===

Index
---
<!-- TOC -->
- [Error in Polynomial Interpolation](#Error-in-Polynomial-Interpolation)
- [Cubic Spline](#Cubic-Spline)
<!-- /TOC -->

## Error in Polynomial Interpolation

Reference STBU 2.1.4

![Error in Poly](images/errorinpoly.jpeg)



[f1]: http://chart.apis.google.com/chart?cht=tx&chl=m=\frac{m_0}{\sqrt{1-{\frac{v^2}{c^2}}}}
[f2]: http://chart.apis.google.com/chart?cht=tx&chl=E_k=mc^2-m_0c^2
[f3]: http://chart.apis.google.com/chart?cht=tx&chl=E=mc^2
[f4]: http://chart.apis.google.com/chart?cht=tx&chl=m_0c^2

## Cubic Spline

### Exists?

![f_c1]

![f_c2]<br>
![f_c3]<br>
![f_c4]<br>
![f_c5]<br>

[f_c1]:http://chart.apis.google.com/chart?cht=tx&chl=P_i(x)=a_ix^3%2Bb_ix^2%2Bc_ix%2Bd_i
[f_c2]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}(x_{i-1})=y_{i-1}
[f_c3]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}(x_{i})=y_{i}
[f_c4]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}'(x_{i})=P_i'(x_{i})
[f_c5]:http://chart.apis.google.com/chart?cht=tx&chl=P_{i-1}''(x_{i})=P_i''(x_{i})