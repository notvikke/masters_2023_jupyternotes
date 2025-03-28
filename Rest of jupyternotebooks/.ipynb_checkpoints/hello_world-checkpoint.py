import sys
import argparse
def main(rep_times,text):
        print(text*rep_times)
    

if __name__ == "__main__":
   

    parser = argparse.ArgumentParser()

    # the arguments we want to catch go here
    parser.add_argument("--n_reps", type=int, required=True, help="no. of reps")
    parser.add_argument("--text", type=str, required=True, help="string req")

    args = parser.parse_args()
    
    main(args.n_reps, args.text)