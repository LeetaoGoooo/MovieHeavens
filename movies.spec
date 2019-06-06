# -*- mode: python -*-

block_cipher = None


a = Analysis(['movies.py', 'movieSource\\MovieHeaven.py', 'movieSource\\fake_user_agent.py'],
             pathex=['F:\\workspace\\python\\MovieHeavens'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='movies',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='resources\\logo.ico')
