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
		name := c.DefaultQuery("name", "ggb")
		level := c.DefaultQuery("level", "SWE")
		pos := c.DefaultQuery("pos", "4029")
		email := c.DefaultQuery("email","854@qq.com")
		state := c.DefaultQuery("state", "on-site")
		waitfor := c.DefaultQuery("waitfor", "15min")
		other := c.DefaultQuery("other", "life_is_nice")
		cmd := exec.Command("python", 
		"/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/update_info.py", 
		"--name="+name, 
		"--level="+level, 
		"--pos="+pos, 
		"--email="+email, 
		"--state="+state, 
		"--waitfor="+waitfor, 
		"--other="+other)	
		cmd.Run()
		c.JSON(200, gin.H{
                        "message": "Update info successful",
                })
	})
        r.Run() // listen and serve on 0.0.0.0:8080
}
