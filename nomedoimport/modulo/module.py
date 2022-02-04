import cv2
from google.cloud import vision
from google.cloud.vision import AnnotateImageResponse
from enum import Enum
import os, errno, json

class FeatureType(Enum):
	PAGE = 1
	BLOCK = 2
	PARA = 3
	WORD = 4
	SYMBOL = 5

class OCR:
	def __init__(self, key_filename):
		self.key_filename = None
		if os.path.isfile(key_filename):
			self.key_filename = key_filename
		else:
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), key_filename)
		
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.key_filename

	def run(self, image, result_json=True):
		if image is None:
			raise AssertionError("Informed image is None")
		
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		_, buff_arr = cv2.imencode('.jpg', image)
		image_bytes = bytes(buff_arr) 
		
		client = vision.ImageAnnotatorClient()
		image_vision = vision.Image(content=image_bytes)
		
		response = client.document_text_detection(image=image_vision, **{"image_context": {"language_hints": ["en-t-i0-handwrit"]}})
		
		if result_json:
			json_response = AnnotateImageResponse.to_json(response)
			json_response = json.loads(json_response)
			json.dumps(json_response)
			return json_response
		else:
			return response

	def parse_ocr_response(self, ocr_response):
		ocr_text_annotation = ""
		if not "fullTextAnnotation" in ocr_response:
			return None

		if len(ocr_response["fullTextAnnotation"]["text"]) == 0:
			return None

		for page in ocr_response["fullTextAnnotation"]["pages"]:
			for block in page["blocks"]:
				for paragraph in block["paragraphs"]:
					for word in paragraph["words"]:	
						ocr_text_annotation += ''.join([symbol["text"] for symbol in word["symbols"]])

		return ocr_text_annotation
	
	def draw_ocr_boxes(self, image, ocr_response):
		word_bounds = self.get_document_bounds(ocr_response, FeatureType.WORD)
		block_bounds = self.get_document_bounds(ocr_response, FeatureType.BLOCK)
		drawn = image.copy()

		for bound in word_bounds:
			drawn = cv2.line(drawn, (bound["vertices"][0]["x"], bound["vertices"][0]["y"]), (bound["vertices"][1]["x"], bound["vertices"][1]["y"]), (0, 76, 244), 2)
			drawn = cv2.line(drawn, (bound["vertices"][1]["x"], bound["vertices"][1]["y"]), (bound["vertices"][2]["x"], bound["vertices"][2]["y"]), (0, 76, 244), 2)
			drawn = cv2.line(drawn, (bound["vertices"][2]["x"], bound["vertices"][2]["y"]), (bound["vertices"][3]["x"], bound["vertices"][3]["y"]), (0, 76, 244), 2)
			drawn = cv2.line(drawn, (bound["vertices"][3]["x"], bound["vertices"][3]["y"]), (bound["vertices"][0]["x"], bound["vertices"][0]["y"]), (0, 76, 244), 2)
		
		for bound in block_bounds:
			drawn = cv2.line(drawn, (bound["vertices"][0]["x"], bound["vertices"][0]["y"]), (bound["vertices"][1]["x"], bound["vertices"][1]["y"]), (255, 255, 0), 2)
			drawn = cv2.line(drawn, (bound["vertices"][1]["x"], bound["vertices"][1]["y"]), (bound["vertices"][2]["x"], bound["vertices"][2]["y"]), (255, 255, 0), 2)
			drawn = cv2.line(drawn, (bound["vertices"][2]["x"], bound["vertices"][2]["y"]), (bound["vertices"][3]["x"], bound["vertices"][3]["y"]), (255, 255, 0), 2)
			drawn = cv2.line(drawn, (bound["vertices"][3]["x"], bound["vertices"][3]["y"]), (bound["vertices"][0]["x"], bound["vertices"][0]["y"]), (255, 255, 0), 2)
		return drawn

	def get_document_bounds(self, response, feature):
		bounds = []

		if not "fullTextAnnotation" in response:
			return bounds
		
		for i, page in enumerate(response["fullTextAnnotation"]["pages"]):
			for block in page["blocks"]:
				if feature == FeatureType.BLOCK:
					bounds.append(block["boundingBox"])
				for paragraph in block["paragraphs"]:
					if feature == FeatureType.PARA:
						bounds.append(paragraph["boundingBox"])
					for word in paragraph["words"]:
						for symbol in word["symbols"]:
							if (feature == FeatureType.SYMBOL):
								bounds.append(symbol["boundingBox"])
						if (feature == FeatureType.WORD):
							bounds.append(word["boundingBox"])
		
		return bounds