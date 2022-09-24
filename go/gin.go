package main

import "github.com/gin-gonic/gin"
import "os/exec"

func main() {
        r := gin.Default()
        r.GET("/", func(c *gin.Context) {
                c.JSON(200, gin.H{
                        "message": "Welcome to e-link! you can use APIs: demo, clear, update_pic, update_info!",
                })
        })
	r.GET("/demo", func(c *gin.Context){
		cmd := exec.Command("python", "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/epd_5in65f_test.py")	
		cmd.Run()
		c.JSON(200, gin.H{
                        "message": "Update successful",
                })
	})
	r.GET("/clear", func(c *gin.Context){
		cmd := exec.Command("python", "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/clear.py")	
		cmd.Run()
		c.JSON(200, gin.H{
                        "message": "Clear successful",
                })
	})
	r.GET("/update_pic", func(c *gin.Context){
		path := c.Query("path")
		cmd := exec.Command("python", "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/update_pic.py", path)	
		cmd.Run()
		c.JSON(200, gin.H{
                        "message": "Update pic successful",
                })
	})
	r.GET("/update_info", func(c *gin.Context){
		icon := c.DefaultQuery("icon", "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/icon.png")
		seat := c.DefaultQuery("seat", "2885")
		name := c.DefaultQuery("name", "Xinyu_Shan")
		rank := c.DefaultQuery("rank", "Support_Engineer")
		team := c.DefaultQuery("team", "PaaS")
		available := c.DefaultQuery("available", "Available")
		position := c.DefaultQuery("position", "WFH")
		phone := c.DefaultQuery("phone", "123546565")
		email := c.DefaultQuery("email", "sky@microsoft.com")
		qrcode := c.DefaultQuery("qrcode", "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/qrcode.png")
		
		cmd := exec.Command("python", 
		"/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/update_info.py", 
		"--icon="+icon,
		"--seat="+seat,
		"--name="+name,
		"--rank="+rank,
		"--team="+team,
		"--available="+available,
		"--position="+position,
		"--phone="+phone,
		"--email="+email,
		"--qrcode="+qrcode)	
		cmd.Run()
		c.JSON(200, gin.H{
                        "message": "Update info successful",
                })
	})
	r.GET("/update_qrcode", func(c *gin.Context){
		path := c.Query("path")
		cmd := exec.Command("python", "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/update_qrcode.py", path)	
		cmd.Run()
		c.JSON(200, gin.H{
                        "message": "Update qrcode successful",
                })
	})
        r.Run() // listen and serve on 0.0.0.0:8080
}
