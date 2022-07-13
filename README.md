# Warm_starting_CG_for_MIO_ML

## Goals ⚽

The aim of this repository is to provide some details of the data sets used in paper [[1]](https://www.researchgate.net/publication/350371853_Machine-learning-aided_warm-start_of_constraint_generation_methods_for_online_mixed-integer_optimization), as well as the code used to obtain the results. This article has been developed by some
members of the [OASYS group](https://sites.google.com/view/groupoasys/home) thanks to the funding of the project [Flexanalytics](https://groupoasysflexanalytics.readthedocs.io/en/latest/). We suggest you visit the related links to know more our research 😉

## How can I download the data? ⬇

Please, click at this [link](https://drive.google.com/drive/folders/1DCaXhlRaZckNaiy6b86CUwzuz1-k-PLS?usp=sharing).

## How can I download the code? ⬇
Please, click at this [link](https://github.com/groupoasys/Warm_starting_CG_for_MIO_ML/tree/main/Code)

## Summary 🧮📊📖

Three cases of study have been analyzed in [[1]](https://www.researchgate.net/publication/350371853_Machine-learning-aided_warm-start_of_constraint_generation_methods_for_online_mixed-integer_optimization): a toy example, a synthetic MILP, and the real-world application, namely the Unit Commitment problem. The data from the toy example can be seen in Section 4 of the paper. In addition, the files of the two large-size data sets are given below:
1) Synthetic MILP:
    * [Objetive function coefficients, c.](https://drive.google.com/file/d/1JfR2j01FNtYmJxPbzR-ryUsOTtPAxaJP/view?usp=sharing)
    * [Matrix coefficients, a.](https://drive.google.com/file/d/1vTVBdi1CYdrdrlLxO82wDLDAhTn7_0U2/view?usp=sharing)
    * [Lower bounds continuous variables, l.](https://drive.google.com/file/d/1oHsUexIvL5FaGGFFIdjAJqHkZltzvkRI/view?usp=sharing)
    * [Upper bounds continuous variables, u.](https://drive.google.com/file/d/1j2e31tO8O27zTow_fir-c7-8Uc2WBZn4/view?usp=sharing)
    * [Independent term, b.](https://drive.google.com/file/d/1koPHTrDGKoLwWNZQWeC-GnqS0EJliv5E/view?usp=sharing)

2) Unit Commitment:
    * [Generators info.](https://drive.google.com/file/d/11o4nx0ca71YmHsTJ1Sde3l6DFAKHwDDn/view?usp=sharing)
    * [Lines info.](https://drive.google.com/file/d/11ow1ZNU_z0ahfYyY0tOYqYgTHsg927uZ/view?usp=sharing)
    * [PTDF info.](https://drive.google.com/file/d/1FRTmX076bCisUp5OrfpjJ358-lJKWePV/view?usp=sharing)
    * [Demand info.](https://drive.google.com/file/d/1EXGqY_-B60ilNiQ5ah2oooWpl8EdXiqY/view?usp=sharing)

## References 📚

[1] Jiménez-Cordero, A., Morales, J.M., & Pineda, S. (2022). Warm-starting constraint generation for mixed-integer optimization: A Machine Learning approach. Submitted. Available [here](https://www.researchgate.net/publication/350371853_Machine-learning-aided_warm-start_of_constraint_generation_methods_for_online_mixed-integer_optimization).

[2] OASYS, Warm_starting_CG_for_MIO_ML, Github repository (https://github.com/groupoasys/Warm_starting_CG_for_MIO_ML), 2022.

## How to cite the repo and the paper? 📝

If you want to cite paper [[1]](https://www.researchgate.net/publication/350371853_Machine-learning-aided_warm-start_of_constraint_generation_methods_for_online_mixed-integer_optimization) or this repo [[2]](https://github.com/groupoasys/Warm_starting_CG_for_MIO_ML), please use the following bib entry:

* Article:
```
@techreport{jimenezcordero2022warm,
  author = {Jim\'enez-Cordero, Asunci\'on and Morales, Juan Miguel and Pineda, Salvador},
  title = {Warm-starting constraint generation for mixed-integer optimization: A Machine Learning approach..},
  institution = {Universidad de M\'alaga},
  year = {2022},
  note = {Available at \url{https://www.researchgate.net/publication/350371853_Machine-learning-aided{\_}warm-start{\_}of{\_}constraint{\_}generation{\_}methods{\_}for{\_}online{\_}mixed-integer{\_}optimization}}}
}
```
* Repository:
```
@article{OASYS2022screening,
author = {OASYS},
journal = {GitHub repository (https://github.com/groupoasys/Warm{\_}starting{\_}CG{\_}for{\_}MIO{\_}ML)},
title = {{Warm_starting_CG_for_MIO_ML}},
url = {https://github.com/groupoasys/Warm{\_}starting{\_}CG{\_}for{\_}MIO{\_}ML},
year = {2022}
}
```

## Do you want to contribute? 🙋‍♀️🙋‍♂️
 
 Please, do it 😋 Any feedback is welcome 🤗 so feel free to ask or comment anything you want via a Pull Request in this repo.
 If you need extra help, you can ask Asunción Jiménez-Cordero (asuncionjc@uma.es), Juan Miguel Morales (juan.morales@uma.es) or Salvador Pineda (spinedamorente@gmail.com).
 
 ## Contributors 🌬☀
 
 * [OASYS group](http://oasys.uma.es) -  groupoasys@gmail.com
 
 ## Developed by 👩‍💻👨‍💻👨‍💻
 * [Asunción Jiménez Cordero](https://www.researchgate.net/profile/Asuncion_Jimenez-Cordero/research) - asuncionjc@uma.es
 * [Juan Miguel Morales](https://www.researchgate.net/profile/Juan_Morales25) - juan.morales@uma.es
 * [Salvador Pineda](https://www.researchgate.net/profile/Salvador_Pineda) - spinedamorente@gmail.com
 
 
 ## License 📝
 
    Copyright 2021 Optimization and Analytics for Sustainable energY Systems (OASYS)

    Licensed under the GNU General Public License, Version 3 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.gnu.org/licenses/gpl-3.0.en.html

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
 

