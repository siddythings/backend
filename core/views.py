from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from django.core.files.storage import default_storage
from uuid import uuid4

import cv2
import imutils
import pytesseract
from pathlib import Path


class CheckNumberPlateView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        number_plate_image = request.FILES.get("number_plate_image")
        if not number_plate_image:
            return Response({"detail": "number_plate_image is required"}, status=HTTP_400_BAD_REQUEST)

        filename = "{}.{}".format(str(uuid4()), number_plate_image.name.split(".")[1])

        with default_storage.open("tmp/" + filename, "wb+") as destination:
            for chunk in number_plate_image.chunks():
                destination.write(chunk)

        # Taking in our image input and resizing its width to 300 pixel
        image = cv2.imread(destination.name)
        image = imutils.resize(image, width=300)

        # Converting the input image to greyscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Reducing the noise in the greyscale image
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

        # Detecting the edges of the smoothened image
        edged = cv2.Canny(gray_image, 30, 200)

        # Finding the contours from the edged image
        cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image1 = image.copy()
        cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)

        # Sorting the identified contours
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        screenCnt = None
        image2 = image.copy()
        cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)

        # Finding the contour with four sides
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4:
                screenCnt = approx

                # Cropping the rectangular part identified as license plate
                x, y, w, h = cv2.boundingRect(c)
                new_img = image[y : y + h, x : x + w]
                cv2.imwrite(destination.name, new_img)
                break

        # Drawing the selected contour on the original image
        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)

        # Extracting text from the image of the cropped license plate
        plate = pytesseract.image_to_string(destination.name, lang="eng")

        # Delete the image from the disk
        Path(destination.name).unlink()

        return Response({"number": plate.strip()})
