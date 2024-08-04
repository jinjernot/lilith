from app.core.models import model
from app.core.xml_parser import process_xml_files_from_folder
from config import XML_PATH

def main():
    process_xml_files_from_folder(XML_PATH, model)

if __name__ == '__main__':
    main()
