import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('creditTD')
    parser.add_argument('creditAE')
    parser.add_argument('debitTD')
    args = parser.parse_args()

    print(args.creditTD, args.creditAE, args.debitTD)