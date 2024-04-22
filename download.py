import requests
import os

# 图片URL列表
image_urls = [
      "https://img10.360buyimg.com/n1/jfs/t1/199841/33/40018/476855/65d2b9c1F9d60678a/507b86ad9aa3d2ba.png.avif",
  "https://img13.360buyimg.com/n1/jfs/t1/234400/19/14301/116901/65d2b9beF2b722dbb/6af3469624512cd3.jpg.avif",
  "https://img12.360buyimg.com/n1/jfs/t1/163360/19/41735/155444/65d2b9c4Fc7b33ab6/f86ccf242e5b4e07.jpg.avif",
  "https://img11.360buyimg.com/n1/jfs/t1/246898/39/5852/122046/65f007d6F4ab1c82d/01f75fe8ea4e9b69.jpg.avif",
  "https://img11.360buyimg.com/n1/jfs/t1/160666/24/42640/150775/65f17c44Fdd2bb03e/319e02d15bac1d3d.jpg.avif",
  "https://img11.360buyimg.com/n1/jfs/t1/148698/40/38773/135704/65f9002aFab69bf76/266eeb3e004ab926.jpg.avif",
  "https://img13.360buyimg.com/n1/jfs/t1/35254/6/16164/101383/659ca038Fa8f6349c/cdb0815654a43661.jpg.avif",
  "https://img14.360buyimg.com/n1/jfs/t1/165261/11/44029/87645/660e587eFb8e99a0f/7966bd6373a32d3a.jpg.avif",
  "https://img12.360buyimg.com/n1/jfs/t1/236237/26/14964/94821/660d29b2F6f1db7ee/52e624fa9cee6b87.jpg.avif",
  "https://img13.360buyimg.com/n1/jfs/t1/234590/12/15417/92531/660d2bf6Fb1a16438/20c30a56980cc4de.jpg.avif",
  "https://img14.360buyimg.com/n1/jfs/t1/188235/6/4111/159640/60a6190bEdf6d1407/937d0e0950969110.jpg.avif",
  "https://img10.360buyimg.com/n1/jfs/t1/207840/24/30028/371697/63e5dd0dFf664944d/d7f4c4791740835a.png.avif",
  "https://p2.itc.cn/q_70/images03/20210301/1e90e57e0d22433c946974cb22975baa.png",
  "https://img13.360buyimg.com/n1/jfs/t1/72186/40/24639/97682/6449c9aeF80046ffa/7b3c8269cf0f32cb.jpg.avif",
  "https://img11.360buyimg.com/n1/jfs/t1/192337/35/42416/95776/660117fbFdbaf211b/5a73413b86100c6c.jpg.avif",
  "https://img14.360buyimg.com/n1/jfs/t1/226046/9/8724/83958/657e44a6F74d1a8d8/de56f91a4b36359a.jpg.avif",
  "https://img14.360buyimg.com/n1/jfs/t1/90658/24/34681/75026/6434c81eF1385a295/657e0c24435cfa03.png.avif",
  "https://img11.360buyimg.com/n1/jfs/t1/226106/21/8772/97012/657e5dfbF8a939174/350834508c253dc8.jpg.avif",
  "https://img12.360buyimg.com/n1/jfs/t1/234608/23/8705/82400/657e6785F16c191b8/a73bf5ab734a0455.jpg.avif",
  "https://img13.360buyimg.com/n1/jfs/t1/229180/39/15201/138556/65f7c65eFfabfd7ea/ba57f29dc92ff984.jpg.avif",
  "https://img13.360buyimg.com/n1/jfs/t1/244769/23/3726/78321/65acd6d3F49b6ad7a/c8e5705c89e7dd6c.jpg.avif",
  "https://img14.360buyimg.com/n1/jfs/t1/237635/18/8631/100920/657e5685F49f02c2b/c2c99f1855625f35.jpg.avif",
  "https://img13.360buyimg.com/n1/jfs/t1/224723/25/8779/42619/657e4fb1Fa2fb0709/da1948125a88d65e.jpg.avif",
  "https://www.fiooo.com/Upload/goods/2018-04/5ac3183eb3f2b.jpg",
  "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F31b787f2-bf15-42d4-93eb-15d6c4f98299%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1715344397&t=a7a8d1f1d01342d8957c82eb52fb4018",
  "https://img1.baidu.com/it/u=398814436,2499206420&fm=253&fmt=auto&app=120&f=JPEG?w=1067&h=800",
    "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F59ce705e-8d16-4cc1-939f-26d8c1b45181%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1715344459&t=94f2fae66f7ccc0ade16a1efeb27f568",
"https://5b0988e595225.cdn.sohucs.com/images/20200305/45df8de20b0c4b5dbd5052eac5ed2f24.JPG",
"https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2Facaf32be-373f-4ad9-bdc6-442fcfd8068c%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1715344499&t=d14ee432202519d6bb261d7f2463cf0d",
"https://d00.paixin.com/thumbs/1177254/40103499/staff_1024.jpg",
"https://img2.baidu.com/it/u=181421418,4273951047&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500",
"https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F17fc6a2c-e735-44c3-9119-8daed8c718e8%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1715344554&t=fee802143e16bb75cf1389548823f731"

    ]

# 图片保存的目录
save_dir = "shoufei"

# 确保保存目录存在
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 下载并保存图片
for i, url in enumerate(image_urls):
    try:
        # 获取图片内容
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功

        # 构建文件名和路径
        file_name = f"{i+1}_fee_{i}.jpg"  # 根据需要调整文件名格式
        file_path = os.path.join(save_dir, file_name)

        # 写入文件
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"图片已下载并保存为：{file_path}")
    except requests.RequestException as e:
        print(f"下载失败：{url}，原因：{e}")

print("所有图片下载完成。")