
def parse_data(file_name):
    output_fp = open("wine_data.csv", "a")

    count = 0
    with open(file_name, "r") as fp:
        line = fp.readline().strip()

        while line:
            if line.startswith("type") or line.startswith("\"fixed"):
                line =  fp.readline().strip()
                continue

            if ";" in line:
                data = line.split(";")
            else:
                data = line.split(",")

            if len(data) == 13:
                print(",".join(data[1:]))
                output_fp.write(",".join(data[1:]) + "\n")
            else:
                print(",".join(data))
                output_fp.write(",".join(data) + "\n")

            count = count + 1
            line = fp.readline().strip()

    return count

def main():
    c = 0
    c = c + parse_data("winequalityN.csv")
    c = c + parse_data("winequality-red.csv")
    c = c + parse_data("winequality-white.csv")

    print("total lines are added: {}".format(c))

if __name__ == "__main__":
    main()