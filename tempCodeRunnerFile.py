    finally:
        # 执行完毕后删除临时文件
        if os.path.exists(filename):
            os.remove(filename)