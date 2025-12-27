# Expressive Movements Creation

Anaelle Jaffré

## Global Methodology

## Script details

### Variables correlation analysis

Some variables are highly correlated with others. for instance, when the robot has the head rather down, then it cannot really rotate it from backwards to forwards.

To be able to see which variables are intrinsically correlated, a Principal Component Analysis (PCA), a method that is usually used in statistics. This can be done with the Python library `sklearn.decomposition`, from which the `PCA` module can be imported.

#### Methodology

The script [`correlation-analysis.py`](correlation-analysis.py) browse a given dataset to make a PCA on the data. It collects the **features** in a vector $X$ containing the following columns:

- x
- y
- z
- roll
- pitch
- yaw
- body_yaw
- ant1 (first antenna)
- ant2 (second antenna)

Then, these variables are standardized, by the following formula:

$X = \frac{X - \mu}{\sigma}$,

with $\mu$ the mean $X$ of the dataset and $\sigma$ the standard deviation. After this, the PCA can be exectued with the line `X = pca.fit_transform(X)`. This allows to project $X$ onto the computed components. Here, `pca` is an instance of the object `PCA`, which has some attributes line the components and variables, and to which are associated some methods, as `fit_transform`.

Finally, the components can be extracted from the object, and shown onto the correlation circle.

**NB:** Two dimensions have been used to represent data, for clarity.

#### Results

The correlation circle obtained from the dataset is the following one:
![Correlation circle](images/correlation_circle.png "Correlation circle")

It can be observed that $pitch$ is highly correlated with $z$, $roll$ with $y$ and $x$ with $yaw$ and $body$ $yaw$.

The antenas do not seem to be correlated with $z$, nor with $x$, due to the angle that is close to 90°. At least, $ant1$ with $x$, and $ant2$ with $yaw$, knowing that $x$ and $yaw$ are highly correlated. However, the do seem to be inversely correlated with $roll$.

|                                        Classic                                         |                     Impact of $roll$                     |                   Impact of $y$                    |
| :------------------------------------------------------------------------------------: | :------------------------------------------------------: | :------------------------------------------------: |
| ![Reachy Mini simulation in the neutral pose](<images/neutral.png>) | ![Reachy Mini simulation while roll is active](images/roll.png) | ![Reachy Mini simulation while y is active](images/y.png) |

It can be confirmed that these variable do influence if the antennas will go through the body of the robot or not, however, so do the other ones, mostly $pitch$ and $yaw$. Hence, the analysis concerning the antennas needs to be reviewed.

In the future, for more precision, it will be possible to proceed to a **multiple linear regression** to analyse the model, so that the most significant variables can be extracted in the interest of the antennas. In a first place, only the 7 other variables will be used to define space constraints.

### Extraction of rules

In order to define the different rules for the robot space, it is necessary to check which position is right, which one is wrong.

As shown in the correlation analysis, $pitch$ is highly correlated with $z$, $roll$ with $y$ and $x$ with $yaw$ and $body$ $yaw$.

Hence, 3 two-by-two dependent rules can be set.

For each of these rules, 3 parameters are calculated, from each pose :

1. The gain $a$,
2. The offset $b$,
3. The standard deviation $sigma$.

#### The gain $a$ (slope)

It represents how much the first variable is influenced by the second one. For instance, for $pitch = a \times z$, it shows how much the head pitch changes when the vertical translation $z$ changes by one unit. If $a$ is really small, $z$ will not have a high influence on the pitch. On the contrary, if $a$ is high, then there is a high geometrical constraint.

#### The offset $b$ (intercept)

It represents the neutral position of the head, when the second variables is equal to 0. For instance, for $pitch = az + b$, then $b$ will be the initial point from where the head will rotate of an $a$ factor towards $z$.

#### The standard deviation $sigma$ (tolerance)

It quantifies possible variability around a neutral pose. For instance, in $pitch = az + b \pm sigma$, $sigma$ defines a tolerance band around the mean relation, within which poses are considered reachable.
