module.exports = {
    outputDir: 'dist',
    assetsDir: 'assets',
    lintOnSave: false,
    devServer: {
        proxy: {
            "/api": {
                target: "http://192.168.3.75:8008"
            },
            "/user": {
                target: "http://192.168.3.75:8008",
            }
        }
    }
}