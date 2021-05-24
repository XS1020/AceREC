module.exports = {
    outputDir: 'dist',
    assetsDir: 'assets',
    lintOnSave: false,
    devServer: {
        proxy: {
            "/api": {
                target: "http://10.164.104.141:8008"
            }
        }
    }
}