import os
import shutil
import zipfile

from awpy.parser import DemoParser

from classification.converter import convert2oneInFolder, eliminateDuplicates, convert2One
from classification.flash_stat import flashStatGenerator
from classification.grenade_stats import grenadeStats
from classification.inertial_shots import inertialShotGenerator
from classification.occluders_generator import occluderGenerator
from classification.onetap_headshot_over_DMG import shotEfficiencyGenerator


def file_name_walk(file_dir):
    for root, dirs, files in os.walk(file_dir):

        for f in files:
            zip_file = zipfile.ZipFile(os.path.join(root, f))
            print(zip_file)
            zip_list = zip_file.namelist()  # 得到压缩包里所有文件

            for ff in zip_list:
                zip_file.extract(ff, root)  # 循环解压文件到指定目录

            zip_file.close()  # 关闭文件，必须有，释放内存


# 挪文件
def copyCertainFiles(source_folder, dest_folder, string_to_match, file_type=None):
    # Check all files in source_folder
    for filename in os.listdir(source_folder):
        # Move the file if the filename contains the string to match
        if file_type == None:
            if string_to_match in filename:
                shutil.move(os.path.join(source_folder, filename), dest_folder)

        # Check if the keyword and the file type both match
        elif isinstance(file_type, str):
            if string_to_match in filename and file_type in filename:
                shutil.move(os.path.join(source_folder, filename), dest_folder)


def generate(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print("root", root)  # 当前目录路径
        print("dirs", dirs)  # 当前路径下所有子目录
        print("files", files)  # 当前路径下所有非目录子文件

        for f in files:
            # Create parser object
            # Set log=True above if you want to produce a logfile for the parser
            if f[-3:] == "dem":
                path = os.path.join(root, f[:-4])
                try:
                    os.makedirs(r'{path}'.format(path=path))
                except FileExistsError:
                    pass
                print("Created :" + path)

                ######################################################################################################################

                ### TODO 这里！！

                # 这里要改成你绝对路径.\demos前的char数量
                # e.g. D:\CSGO_Aanlysi\s  这里为17位
                #      D:\CSGO_Aanlysis\demos\S_plus\g151-c-20230129224454840798337_de_inferno
                # dmf = ".\\" + root[17:] + "\\" + f
                dmf = os.path.join(root, f)
                print("Current .dem: " + dmf)
                demo_parser = DemoParser(
                    demofile=r'{dmf}'.format(dmf=dmf),
                    parse_rate=1,
                )

                df = demo_parser.parse(return_type="df")

                df["kills"].to_csv(demo_parser.demo_id + "_kills.csv", encoding="utf_8_sig")
                df["damages"].to_csv(demo_parser.demo_id + "_damages.csv", encoding="utf_8_sig")
                df["weaponFires"].to_csv(demo_parser.demo_id + "_weaponFires.csv", encoding="utf_8_sig")
                df["rounds"].to_csv(demo_parser.demo_id + "_rounds.csv", encoding="utf_8_sig")
                df["grenades"].to_csv(demo_parser.demo_id + "_grenades.csv", encoding="utf_8_sig")
                df["flashes"].to_csv(demo_parser.demo_id + "_flashes.csv", encoding="utf_8_sig")
                df["frames"].to_csv(demo_parser.demo_id + "_frames.csv", encoding="utf_8_sig")
                df["playerFrames"].to_csv(demo_parser.demo_id + "_playerFrames.csv", encoding="utf_8_sig")

                copyCertainFiles(root, path, f[:-4], file_type=None)


def delete(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print("root", root)  # 当前目录路径
        print("dirs", dirs)  # 当前路径下所有子目录
        print("files", files)  # 当前路径下所有非目录子文件

        for f in files:
            if f[-3:] == "dem":
                os.remove(os.path.join(root, f))
            if f[-4:] == "json":
                os.remove(os.path.join(root, f))


def move(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print("root", root)  # 当前目录路径
        print("dirs", dirs)  # 当前路径下所有子目录
        print("files", files)  # 当前路径下所有非目录子文件

        # TODO HERE
        copyCertainFiles(root, r"D:\CSGO_Aanlysis\demos\S_plus", ".zip", file_type=None)


######################################################################################################################

### TODO 还有这里！！ 存放的根目录

def main(dir):
    # 解压zip
    file_name_walk(dir)
    # 生成文件
    generate(dir)
    # 删除dem&json
    delete(dir)
    flashStatGenerator(dir)
    grenadeStats(dir)
    inertialShotGenerator(dir)
    occluderGenerator(dir)
    shotEfficiencyGenerator(dir)
    convert2oneInFolder(dir)
    convert2One(dir)
    eliminateDuplicates(dir)

# # 重置 demo位置
# move("D:\CSGO_Aanlysis\demos\S_plus")
