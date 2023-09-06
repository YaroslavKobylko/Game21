#include <vector>
#include <string>
#include <algorithm>
#include <random>

class Game {
private:
    std::vector<const char*> deck;
    std::vector<const char*> playerHand;
    std::vector<const char*> botHand;
    int playerHandSize;
    int botHandSize;

public:
    Game() {
        playerHandSize = 0;
        botHandSize = 0;
    }

    std::vector<const char*> shuffleDeck() {
        std::vector<const char*> temp(deck);
        std::random_device rd;
        std::mt19937 gen(rd());
        std::shuffle(temp.begin(), temp.end(), gen);
        return temp;
    }

    void dealCards() {
        playerHand[playerHandSize] = deck.back();
        playerHandSize++;
        deck.pop_back();

        playerHand[playerHandSize] = deck.back();
        playerHandSize++;
        deck.pop_back();

        botHand[botHandSize] = deck.back();
        botHandSize++;
        deck.pop_back();

        botHand[botHandSize] = deck.back();
        botHandSize++;
        deck.pop_back();
    }

    int calculateScore(const std::vector<const char*>& hand) {
        int score = 0;
        int numAces = 0;
        for (const char* card : hand) {
            char rank = card[1]; 
            if (rank == 'J' || rank == 'Q' || rank == 'K' || rank == 'T') {
                score += 10;
            }
            else if (rank == 'A') {
                score += 11;
                numAces++;
            }
            else {
                int cardValue = atoi(&rank);  
                score += cardValue;
            }
        }

        while (score > 21 && numAces > 0) {
            score -= 10;
            numAces--;
        }

        return score;
    }
};