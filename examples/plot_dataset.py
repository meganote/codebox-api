from pathlib import Path

import requests

from codeboxapi import CodeBox

with CodeBox() as codebox:
    # download the iris dataset
    csv_bytes = requests.get(
        "https://archive.ics.uci.edu/" "ml/machine-learning-databases/iris/iris.data"
    ).content

    print("downloaded dataset")

    # upload the dataset to the codebox
    o = codebox.upload("iris.csv", csv_bytes)

    # dataset analysis code
    file_path = Path("examples/assets/dataset_code.txt")

    # run the code
    output = codebox.run(file_path=file_path)
    print(output.type)

    if output.type == "image/png":
        # Convert the image content into an image
        import base64
        from io import BytesIO

        try:
            from PIL import Image  # type: ignore
        except ImportError:
            print(
                "Please install it with "
                '`pip install "codeboxapi[image_support]"`'
                " to display images."
            )
            exit(1)

        # Decode the base64 string into bytes
        img_bytes = base64.b64decode(output.content)

        # Create a BytesIO object
        img_io = BytesIO(img_bytes)

        # Use PIL to open the image
        img = Image.open(img_io)

        # Display the image
        img.show()

    elif output.type == "error":
        # error output
        print("Error:")
        print(output.content)

    else:
        # normal text output
        print("Text Output:")
        print(output.content)