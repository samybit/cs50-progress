#include <cs50.h>
#include <stdio.h>

// function pattern
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Prompt the user for change owed, in cents
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int coins = 0;

    // | Calculate how many ¢ you should give customer |
    // | And Subtract the value of those ¢ from cents  |
    int quarters = calculate_quarters(cents);
    cents -= quarters * 25;
    coins += quarters;

    int dimes = calculate_dimes(cents);
    cents -= dimes * 10;
    coins += dimes;

    int nickels = calculate_nickels(cents);
    cents -= nickels * 5;
    coins += nickels;

    int pennies = calculate_pennies(cents);
    cents -= pennies * 1;
    coins += pennies;

    printf("%i\n", coins);
}

int calculate_quarters(int cents)
{
    // Calculate how many quarters you should give customer
    int quarters = 0;
    while (cents >= 25)
    {
        quarters++;
        cents -= 25;
    }
    return quarters;
}

int calculate_dimes(int cents)
{
    // Calculate how many dimes you should give customer
    int dimes = 0;
    while (cents >= 10)
    {
        dimes++;
        cents -= 10;
    }
    return dimes;
}

int calculate_nickels(int cents)
{
    // Calculate how many nickels you should give customer
    int nickels = 0;
    while (cents >= 5)
    {
        nickels++;
        cents -= 5;
    }
    return nickels;
}

int calculate_pennies(int cents)
{
    // Calculate how many pennies you should give customer
    int pennies = 0;
    while (cents >= 1)
    {
        pennies++;
        cents -= 1;
    }
    return pennies;
}
