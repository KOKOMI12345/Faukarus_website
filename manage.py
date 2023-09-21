from program import *

#这个以后作为启动入口
if __name__ == '__main__':
 try:
    playsound("F:/Faukarus_music_site/Fukarus_voice/ready_to_start_F.wav")
    playsound("F:/Faukarus_music_site/Fukarus_voice/20s_F.wav")
    app.logger.info("服务器启动将在倒计时20秒后.....")
    time.sleep(20)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    app.logger.info("服务器已启动")
    playsound("F:/Faukarus_music_site/Fukarus_voice/start_success.wav")
    server.serve_forever()
 except Exception as e:
    app.logger.warning("警告服务器启动失败!")
    playsound("F:/Faukarus_music_site/Fukarus_voice/太阳晒屁股啦!.wav")
    app.logger.error("服务器意外关闭")
    app.logger.info("由于一个不可抗的异常或手动关停,导致了程序结束")
    app.logger.error(e)
    #print(e)