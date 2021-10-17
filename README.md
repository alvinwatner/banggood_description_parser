## Purpose
The purpose of this repository is to extract the description content from banggood marketplace.

## Who will benefit from this project:
The people that intend to Dropship the product from Banggood to other local market place (for e.g., Tokopedia, Bukalapak)

## Challenges:
* The products page dynamically changing from one to another.
* Inconsistency html script.
* Inconsistency description titles (for e.g., Product 1 had title : "Package Include" while product 2 : "Package Includes").
* The content description that formed in table require extra postprocessing to transformed it intro readable text.

## Objective:
* To create an algorithm that able to identify the variety of description contents (for e.g., Features, specifications) and extract the content within while maintaining the readability of the extracted result.
* Maximize the number of "identified contents" and improve the readbility as indication of robust algorithm.

## Future to-do list:
1. Improve the sanity check - What I had in mind :
    1. Add flag to mark the unidentified content. 
    2. Create a file that stored the **lowest** number of flag from N number of sample test.
    3. For every updated algorithm, run a script that compare the output with the **lowest**.
    4. If the updated algorithm ouput lower than the previous **lowest**, then it approved to
	      perform better.


## Authors Info
```
----------------------------------------
Author  : Alvin Watner
Email   : alvinsetiadi22@gmail.com
Website : -
License : MIT
----------------------------------------
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
