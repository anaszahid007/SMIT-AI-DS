try:
    # Added encoding='utf-8' to handle special characters correctly
    with open("read.txt", "w", encoding="utf-8") as f:
        f.write("hellow world!")


except FileNotFoundError:
    print("File Not Found!")

except Exception:
    print("Something went wrong")
