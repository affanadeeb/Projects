// Fractions.cpp

#include "Fractions.hpp"
#include <bits/stdc++.h>

template <typename T>
T gcd(T a, T b) {
    return b ? gcd<T>(b, a % b) : a;
}

// Constructor
template <typename T>
Fraction<T>::Fraction(T num, T denom) : numerator(num), denominator(denom) {}

// Reduction of fraction
template <typename T>
Fraction<T> Fraction<T>::reduce() {
    T G = gcd(numerator, denominator);
    numerator = numerator / G;
    denominator = denominator / G;
    if (numerator < 0 && denominator < 0) {
        numerator = -numerator;
        denominator = -denominator;
    } else if (denominator < 0) {
        denominator = -denominator;
        numerator = -numerator;
    }
    return *this;
}

// Implementation of getters
template <typename T>
T Fraction<T>::get_numerator() {
    return numerator;
}

template <typename T>
T Fraction<T>::get_denominator() {
    return denominator;
}

// Addition
template <typename T>
Fraction<T> Fraction<T>::operator+(Fraction<T>& other) {
    T lcm = (denominator * other.denominator) / gcd(denominator, other.denominator);
    T num = (numerator * lcm / denominator) + (other.numerator * lcm / other.denominator);
    Fraction<T> ans(num,lcm);
    return ans.reduce();
}

// Subtraction
template <typename T>
Fraction<T> Fraction<T>::operator-(Fraction<T>& other) {
    T lcm = (denominator * other.denominator) / gcd(denominator, other.denominator);
    T num = (numerator * lcm / denominator) - (other.numerator * lcm / other.denominator);
    Fraction<T> ans(num,lcm);
    return ans.reduce();
}

// Multiplication
template <typename T>
Fraction<T> Fraction<T>::operator*(Fraction<T>& other) {
    T num = numerator * other.numerator;
    T denom = denominator * other.denominator;
    Fraction<T> ans(num,denom);
    return ans.reduce();
}

// Division
template <typename T>
Fraction<T> Fraction<T>::operator/(Fraction<T>& other) {
    T num = numerator * other.denominator;
    T denom = denominator * other.numerator;
    Fraction<T> ans(num,denom);
    return ans.reduce();
}

// Comparison operators

// Equal
template <typename T>
bool Fraction<T>::operator==(Fraction<T>& other) {
    Fraction<T> reduced_this = reduce();
    Fraction<T> reduced_other = other.reduce();
    return (reduced_this.numerator == reduced_other.numerator && reduced_this.denominator == reduced_other.denominator);
}

// Unequal
template <typename T>
bool Fraction<T>::operator!=(Fraction<T>& other) {
    return !(*this == other);
}

// Less than or equal
template <typename T>
bool Fraction<T>::operator<=(Fraction<T>& other) {
    Fraction<T> reduced_this = reduce();
    Fraction<T> reduced_other = other.reduce();
    return (reduced_this.numerator * reduced_other.denominator <= reduced_other.numerator * reduced_this.denominator);
}

// Less than
template <typename T>
bool Fraction<T>::operator<(Fraction<T>& other) {
    Fraction<T> reduced_this = reduce();
    Fraction<T> reduced_other = other.reduce();
    return (reduced_this.numerator * other.denominator < reduced_other.numerator * reduced_this.denominator);
}

// Greater than or equal
template <typename T>
bool Fraction<T>::operator>=(Fraction<T>& other) {
    Fraction<T> reduced_this = reduce();
    Fraction<T> reduced_other = other.reduce();
    return (reduced_this.numerator * reduced_other.denominator >= reduced_other.numerator * reduced_this.denominator);
}

// Greater than
template <typename T>
bool Fraction<T>::operator>(Fraction<T>& other) {
    Fraction<T> reduced_this = reduce();
    Fraction<T> reduced_other = other.reduce();
    return (reduced_this.numerator * reduced_other.denominator > reduced_other.numerator * reduced_this.denominator);
}

// Implementing the print() function
template <typename T>
void Fraction<T>::print() {
    Fraction<T> reduced_fraction = reduce();
    std::cout << reduced_fraction.numerator << div_char << reduced_fraction.denominator << std::endl;
}