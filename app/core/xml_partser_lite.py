import os
import xml.etree.ElementTree as ET
import pandas as pd
from config import HTML_TEMPLATE_LITE, OUTPUT_PATH, EXCEL_FILE_NAME, HTML_FILE_NAME

def process_data(folder_path):
    all_image_data = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.xml'):
            xml_file_path = os.path.join(folder_path, filename)
            try:
                tree = ET.parse(xml_file_path)
                root = tree.getroot()
            except ET.ParseError:
                print(f"Error parsing the XML file '{filename}'. Skipping.")
                continue

            # Extract filename without extension
            base_filename = os.path.splitext(filename)[0]

            # Create an empty list
            image_data = []

            # Get the prodnum
            prodnum_element = root.find(".//product_numbers/prodnum")
            prodnum = prodnum_element.text.strip() if prodnum_element is not None else ""

            # Loop through all the required elements
            for asset_element in root.findall(".//image"):
                asset_embed_code_element = asset_element.find("image_url_https")
                orientation_element = asset_element.find("orientation")
                master_object_name_element = asset_element.find("master_object_name")
                pixel_height_element = asset_element.find("pixel_height")
                pixel_width_element = asset_element.find("pixel_width")
                content_type_element = asset_element.find("content_type")
                document_type_detail_element = asset_element.find("document_type_detail")
                cmg_acronym_element = asset_element.find("cmg_acronym")
                color_element = asset_element.find("color")

                # Check if 'image_url_https' and 'product image' or 'product in use' is available
                if asset_embed_code_element is not None and document_type_detail_element is not None:
                    image_url = asset_embed_code_element.text.strip()
                    document_type_detail = document_type_detail_element.text.strip()

                    # Get the elements
                    if image_url and document_type_detail in ["product image", "product in use"]:
                        orientation = orientation_element.text.strip() if orientation_element is not None else ""
                        master_object_name = master_object_name_element.text.strip() if master_object_name_element is not None else ""
                        pixel_height = pixel_height_element.text.strip() if pixel_height_element is not None else ""
                        pixel_width = pixel_width_element.text.strip() if pixel_width_element is not None else ""
                        content_type = content_type_element.text.strip() if content_type_element is not None else ""
                        cmg_acronym = cmg_acronym_element.text.strip() if cmg_acronym_element is not None else ""
                        color = color_element.text.strip() if color_element is not None else ""

                        image_data.append({
                            "prodnum": prodnum,
                            "url": image_url,
                            "orientation": orientation,
                            "master_object_name": master_object_name,
                            "pixel_height": pixel_height,
                            "pixel_width": pixel_width,
                            "content_type": content_type,
                            "document_type_detail": document_type_detail,
                            "cmg_acronym": cmg_acronym,
                            "color": color
                        })

                        # Append data to the list
                        all_image_data.append({
                            "prodnum": prodnum,
                            "url": image_url,
                            "orientation": orientation,
                            "master_object_name": master_object_name,
                            "pixel_height": pixel_height,
                            "pixel_width": pixel_width,
                            "content_type": content_type,
                            "document_type_detail": document_type_detail,
                            "cmg_acronym": cmg_acronym,
                            "color": color
                        })

    # Sort image data by document type detail
    image_data = sorted(all_image_data, key=lambda x: x["document_type_detail"])

    # Read the template file
    with open(HTML_TEMPLATE_LITE, 'r') as file:
        html_template = file.read()

    # Generate HTML table rows
    previous_type = None
    table_rows = ""
    for data in image_data:
        if previous_type is not None and previous_type != data['prodnum']:
            # Add <hr> to separate different document types
            table_rows += """
            <tr>
                <td colspan="12"><hr class="divider"></td>
            </tr>
            """

        table_rows += f"""
        <tr>
            <td>{data['prodnum']}</td>
            <td>{data['url']}</td>
            <td>{data['orientation']}</td>
            <td>{data['master_object_name']}</td>
            <td>{data['pixel_height']}</td>
            <td>{data['pixel_width']}</td>
            <td>{data['content_type']}</td>
            <td>{data['document_type_detail']}</td>
            <td>{data['cmg_acronym']}</td>
            <td>{data['color']}</td>
            <td><img src='{data['url']}' alt='Image' width='300' height='300'></td>
        </tr>
        """

        previous_type = data['prodnum']

    # Replace placeholder with the generated rows
    html_content = html_template.replace('{{ table_rows }}', table_rows)

    # Create a DataFrame from the image data
    df = pd.DataFrame(all_image_data)

    # Identify duplicate rows
    duplicates = df.duplicated(subset=["prodnum", "orientation", "pixel_height", "content_type", "cmg_acronym", "color"], keep=False)

    # Add a new column "note" and set it to "duplicate" for duplicate rows
    df['note'] = ''
    df.loc[duplicates, 'note'] = 'duplicate'

    # Save the DataFrame to an Excel file
    excel_path = os.path.join(OUTPUT_PATH, EXCEL_FILE_NAME)
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

    # Save the HTML content to a file
    html_path = os.path.join(OUTPUT_PATH, HTML_FILE_NAME)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Processed {len(all_image_data)} images. Output saved to '{excel_path}' and '{html_path}'.")