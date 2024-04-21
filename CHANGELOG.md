# Changelog

## 1.2.4 (2024/04/21)
### ✨ Enhancements
- [Add support for setting cover (tilt) position](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/6f730d6a85e54c4058133a540be5b91f147d52fa) - @RogerSelwyn

### 🔖 Release
- [v1.2.4](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/efba312c6897dd9c04d367a355a7487136410ff3) - @RogerSelwyn

## 1.2.3 (2024/04/20)
### 🐛 Fixes
- [Fix incorrect subscription before MQTT available](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/364d989e97dbf3f61203f400bd4c801a346a21e1) - @RogerSelwyn

### 🧰 Maintenance
- [Even more code de-duplication](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/b8f64654f089ea17e4d42bba7132efba86d96da1) - @RogerSelwyn
- [Make entity type translation more generic](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/b05198ec7927b3529f2b0c329e27749b8348613d) - @RogerSelwyn
- [Optimise code to reduce unnecessary imports](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/3f0c572523fdb1d39a45ee4bb2665f4758ed5cfb) - @RogerSelwyn

### 🔖 Release
- [Release v1.2.3](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/0a02f1bb97eebde673941c2da4a577f5e8d945fb) - @RogerSelwyn


## 1.2.2 (2024/04/18)
### 🧰 Maintenance
- [Further code de-duplication](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/61b7260c6da7f90eb3a1be27b3368415eda73771) - @RogerSelwyn
- [Code cleanup](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/ab8b7eb9774bb97a422881cd8a6e19c6b34ba39c) - @RogerSelwyn
- [Major de-duplication of code to aid readability](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/da01dfa5ea43a82dbb66a0cb8c86afaa2af82e0c) - @RogerSelwyn
- [Further code removal](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/88d7ee73b73551bb6cc308711b0bbd8ae917598f) - @RogerSelwyn

### 🔖 Release
- [v1.2.2](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/05b37df7f813ef28e682f05b4d739187651044ac) - @RogerSelwyn

## 1.2.1 (2024/04/17)
### 🧰 Maintenance
- [Only subscribe to required topics](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/1a6081a1db368f8bac2dd2ddd05681f46317ed4f) - @RogerSelwyn
- [Remove publication of unrequired attribute](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/d09958facce302a809b57fd21a0f78ff83105937) - @RogerSelwyn
- [Simplify subscription code](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9c8168633d36dbcfa99d6a7ffab2b7a50d9a4a32) - @RogerSelwyn

### 📚 Documentation
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/0276256925a54be994a673315dda9276e70c5608) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5b51e28e03fa698d03fdb4cc0806a59fa583dff5) - @RogerSelwyn

### 🔖 Release
- [Release v1.2.1](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/b18669e2c61419c4fc2e4b9f707c026d6c9ba955) - @RogerSelwyn

## 1.2.0 (2024/04/16)
### ✨ Enhancements
- [Add support for input_select](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/c188cc48cc4f7351cd3ca9cc0c3131afff5409a3) - @RogerSelwyn

### 🔖 Release
- [Release v1.2.0](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/29f19c3922fbcdf647f1be56db8e584083ff0781) - @RogerSelwyn

## 1.1.3 (2024/04/03)
### 💥 Breaking Changes
Home Assistant 2024.4.0 introduces a change that break this integration. You will need to upgrade to this release when upgrading to 2024.4.0.

- [Change in support of HA core breaking change in 2024.4](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/96210fa40be45653df7b6ed2915a4b0cb87d92e8) - @RogerSelwyn

### ✨ Enhancements
- [Add service icon](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/7a43cc4fce1bd681b1aaa64d3b40ef140847b6ab) - @RogerSelwyn
- [Add support for light effects](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8a84e0490f7b60b760299d72d53cebf71a199507) - @RogerSelwyn

### 🐛 Fixes
- [Remove unrequired climate state subscription (uses mode)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8f306e28c523383736ebcd725e344797dd55eed1) - @RogerSelwyn

### 🧰 Maintenance
- [Remove deprecated color_mode attribute from light](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/dae0bdf3d2efd12c397a0bebaffa4aae483c2259) - @RogerSelwyn
- [Set minimum to 2024.4.0](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9b77daf03583fd3d3c9981a14cb513cd308b02da) - @RogerSelwyn

### 📚 Documentation
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/6165beddd6df2330c16d74bfdf28f10d1a104d8d) - @RogerSelwyn
- [Updated Mermaid diagrams with more detail](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/4d0deda014252962440444ef1a3d4bd0d0044bae) - @RogerSelwyn

### 🔖 Release
- [Release v1.1.3](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/4b3a2c482e29b1afd719ee6ecdfa91751c34f59c) - @RogerSelwyn

## 1.1.2 (2024/03/26)
### ✨ Enhancements
- [Mark entities unavailable at HA shutdown](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e1c7334b9979bc375a848e7c92e79a871fe8fce7) - @RogerSelwyn

### 🔖 Release
- [Auto update manifest.json](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/d0556eca7bdd295a19ca3d34f4e59c4bf7256570) - @actions-user
- [Release v1.1.2](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e4c517a4554c46270dc9ee8fe1878a45b6b9cb70) - @RogerSelwyn

## 1.1.1 (2024/03/25)
### 🐛 Fixes
- [Change online status subscribe to `latest` instead of `all`](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/47e95d5260cd6656ee91a737653eaa294333b3cd) - @RogerSelwyn

### 🔖 Release
- [Release v1.1.1](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/fdad0a7d894703d74482dac2509075694fb682e9) - @RogerSelwyn

## 1.1.0 (2024/03/25)
### 💥 Breaking Changes
- [Add ability to make slave entities unavailable if master offline](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/d9385e52d989c20c1ff222265f11db08a48528fd) - @RogerSelwyn

### ✨ Enhancements
- [Add scheduled re-publishing of discovery/state](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/6a62f0b818c5c16b68c737d5609d360e1e269ce8) - @RogerSelwyn

### 🧰 Maintenance
- [Correct location of GitHub repository](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8ecafe234df6b41893eccc39d99ed92b80d78078) - @RogerSelwyn

### 🔖 Release
- [Release v1.1.0](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/82729f2dd212f2966b237750c4af833bdf184831) - @RogerSelwyn

## 1.0.2 (2024/03/17)
### 🐛 Fixes
- [Fix issue with color_mode (not deprecated yet)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/bff7d9d93ba40207de4480ee97e6acef646b51cb) - @RogerSelwyn

### 📚 Documentation
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/fbd42bc91e23fb86666bac34c1780f9373dfdc29) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/0b6f3549ee69d62084c5312411005bcab531f34d) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/ecde8334dd562d6a6b64f3a0b0dc5d45dc61435f) - @RogerSelwyn

### 🔖 Release
- [Release v1.0.2](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/36c5eadeef0e6a7b6c66f41cdb1364d9b53bd2cf) - @RogerSelwyn

## 1.0.1 (2024/03/12)
### 💥 Breaking Changes
- [Set retain bit on messages to False](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/c4a1deeaed24b4b022f89bfef5fd553f194c572c) - @RogerSelwyn

### 🐛 Fixes
- [Fix issue with entity registry changing during publish](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9fad04fc93c64a74c4ac8f57252f533c13f2b0fb) - @RogerSelwyn
- [Fix state publishing after birth discovery publish](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/ad6569ed4e77e08c60f3f11c1be1db558b7d48a0) - @RogerSelwyn

### 🔖 Release
- [Release v1.0.1](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e15855fa1eef53224ab5c84c1464461a2a6ced31) - @RogerSelwyn

## 1.0.0 (2024/03/11)
### ✨ Enhancements
- [Subscribe to Birth messages to initiate Discovery](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9218d299e4ca86162a6a271e4f292f6dc0985517) - @RogerSelwyn

### 🧰 Maintenance
- [Change lwt to birth](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/fcdf39c802795b8a310fbd4b641b79cd237de3cb) - @RogerSelwyn

### 📚 Documentation
- [Added flowcharts](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/1fef1e59f375d80a5142f1a2281c5b7f3a8315e6) - @RogerSelwyn
- [Updated flowcharts](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/bd390e59db762d1618e7c643b89a0e47b6393f62) - @RogerSelwyn

### 🔖 Release
- [Release v1.0.0](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/1a0a38ce93e8a3f49f7154018902fc638332b0f4) - @RogerSelwyn

## 0.12.00 (2024/03/10)
### ✨ Enhancements
- [Add service to trigger re-publication of discovery and state information](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/08c39e65ff2e2d7a5aabf34c3eb4f22ae88532fe) - @RogerSelwyn
- [Add publication of discover and current state after HA startup](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e308f5deded08a1ce38bec20d22974feb3d2683a) - @RogerSelwyn

### 🧰 Maintenance
- [Add services.yaml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5d5ee5a10dfabdfd9ac7e952ccf051e0763b8487) - @RogerSelwyn

### 📚 Documentation
- [Update CHANGELOG.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/32f16334e5bbfeb5a7eed4dba07e9c2dd0f2ab5a) - @RogerSelwyn

### 🔖 Release
- [Release v0.12.00](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/f99f7b883580137125c1beceb69d3e614d3e8046) - @RogerSelwyn

## 0.11.05 (2024/03/05)
### 🐛 Fixes
- [Fix warning from deprecation of color_mode flag](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5a23cbf018f38feaa2ea93a50227c3d6fcdf6032) - @RogerSelwyn

### 🔖 Release
- [Release v0.11.05](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/12f7732adf8745857bc29a438c325b75092b7d44) - @RogerSelwyn

## 0.11.04 (2024/03/02)
### 🐛 Fixes
- [Fix deprecation alert for MQTT component usage](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/4a68373788ab97589391d1a8c79a7f6b18956776) - @RogerSelwyn

### 🔨 Maintenance
- [Code improvement](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/cdf0bebd9820f6ada8832ee356cca3b7915662b3) - @RogerSelwyn

### 🔖 Release
- [Release v0.11.04](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9bab85c66791bbbd78e2dc6f6ab1442d110a02ec) - @RogerSelwyn

## 0.11.03 (2024/01/16)
### 🐛 Fixes
- [Handle changes in core related to attribute passing](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9b0e1859a1f2d30d488fc11a9a3b26680a457621) - @RogerSelwyn
- [Handle changes in core related to attribute passing](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/c60675989badc48a1845947414769b5789a0abc2) - @RogerSelwyn
- [Only handle service calls for discoveries we published](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e8646abb05466052ac26928f960270699f78ac76) - @RogerSelwyn

### 📚 Documentation
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/43ba493c8a73ca073199a4b8c19022c8ebd8d2c4) - @RogerSelwyn

### 🔖 Release
- [Release v0.11.03](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/bf2a8750fc7ae30a510fd889adfc1500af32000a) - @RogerSelwyn

## 0.11.02 (2023/10/04)
### 🐛 Fixes
- [Fix mqtt errors when entity unavailable. Don't publish state, just availability](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8ac141768fb2096127b7153e7eec7a9f44d35967) - @RogerSelwyn

### 🔨 Maintenance
- [Update dependabot.yml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/d777274d247d86fe6b8940351dcd230a1b6d76a6) - @RogerSelwyn
- [Bump to v0.11.02](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9ab1afba8e05b85c34184f4334b4c4763e978dca) - @RogerSelwyn
- [Bump actions/checkout from 2 to 4](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/a72527d098c095acbb67ca64dcb6fe760c2e772c) - @dependabot[bot]

## 0.11.01 (2023/09/13)
## ✨ Enhancements
- [Add suggested_display_precision to sensor](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5e4ec8a139606ea22d5fb5c3f4d2b6bbbee54b4b) - @RogerSelwyn

### 🐛 Fixes
- [Fix topic prefix validation](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/62b2ea4026c44d92481c3aefdc39b173e98fab7f) - @miguelangel-nubla
- [Add back empty requirements](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9091665f78519350d032ff9f2af4feb583a61a51) - @RogerSelwyn

### 🔨 Maintenance
- [Bump to v0.11.01](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/1be24e2169602e6fd433a4ae9c0f87c1149ed477) - @RogerSelwyn
- [Remove numpy as requirement](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/18dc2a3f2fa61e464fc8fa45e4116c31d563908f) - @RogerSelwyn

## 0.11.00 (2023/08/22)
### Maintenance
- [Split discovery publishing from state publishing for ease of maintenance](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/47b3949013e7bc5b472056c67330951ee8c30b86) - @RogerSelwyn
- [Bump to v0.11.00](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/1a5a83e42552dfe6fa9af4ddbebeeb9db28e3f3f) - @RogerSelwyn

## 0.10.13 (2023/08/03)
### Fixes
- [Fix AttributeError: 'NoneType' object has no attribute 'entity_category'](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/382503aa8a4818785f6d470a02a56a8e0bf31852) - @RogerSelwyn

### Maintenance
- [Bump to v0.10.13](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e86c5e0400c052666d23ee6de8e10ed7bdcb7336) - @RogerSelwyn

## 0.10.12 (2023/08/03)
### Fixes
- [Fix AttributeError: 'NoneType' object has no attribute 'device_id'](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8f9eaa0b4002303e7aa9758df824abcb513215f1) - @RogerSelwyn 

### Maintenance
- [Bump to v0.10.12](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8052517038ebb94eb421edcb40aef3cdd4bd51e1) - @RogerSelwyn

## 0.10.11 (2023/08/03)
### Maintenance
- [Improve entity naming validation](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/911f7358d126638033692754cdb77dc063faeb2e) - @RogerSelwyn
- [Bump to v0.10.11](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/2b6108415019ce07339711c98e51eb1be569da3f) - @RogerSelwyn

## 0.10.10 (2023/08/03)
### Fixes
- [Correct the sending of entity name for 2023.8.0](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/58bc723b44d590d8dd344da20a914dbcef5e3b86) - @RogerSelwyn

### Maintenance
- [Remove redundant code](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/986d08c2cd1241467113bd53e9138f000763db49) - @RogerSelwyn
- [Update validate_hacs.yaml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/3f788964de1a7a59ffacf1bac2addedd670ce0d1) - @RogerSelwyn
- [Bump to v0.10.10](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5af73d48c834eaae667cc4bf01d80ad598feff72) - @RogerSelwyn

### Documentation
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e7db855b39f36362a22b2544321d41a4024fb928) - @RogerSelwyn
- [Update README.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/03b35f3183b9ab3383ee47e8cf9a816495eb47f8) - @RogerSelwyn

## 0.10.9 (2023/07/01)
### Maintenance
- [Standardise method of waiting for MQTT client](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/3d248d20b3c148355145c7bc8a31e2e050c34f7b) - @RogerSelwyn
- [Update in line with changes to Koyring version](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/ab7ebda3156f870439c5eef664d1f8496d3bc089) - @RogerSelwyn
- [Bump to v0.10.9](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/bae44af02f079f0665a40a48e45eeba2898b80f8) - @RogerSelwyn

## 0.10.8 (2023/04/23)
### Enhancements
- [Add support for covers (open/close)](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/pull/2) - @pergolafabio
- [Improve Cover entity type addition](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5d73e17e308f0d9841b9e564cc0063827743442c) - @RogerSelwyn

### Maintenance
- [Keep in line with core mqtt_statestream](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/34459e78b0fb633a9d70786725bdc1ad6a4ba6c2) - @RogerSelwyn
- [Revert change](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/bab801d8e988f7e59e32070acc16379bbd642856) - @RogerSelwyn
- [Bump to v0.10.8](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/ed4d7dd27c52a802c8c8ce0492fb843d24370476) - @RogerSelwyn


## 0.10.7 (2023/03/22)
### Maintenance
- [Create stale.yml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/6186f6713bfc4b6283bd5a115d6cdaa22daa6f9f) - @RogerSelwyn
- [Create dependant.yml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/91d048dc3bc8d8c2fe3f35e35caec74e6ae69637) - @RogerSelwyn
- [Create dependabot.yml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/246ef7ac15d1abe2edfb23ee9a29c5d9535d01e8) - @RogerSelwyn
- [Delete dependant.yml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/d09decd0e22e6b9a1b69c537e41b021219bab70c) - @RogerSelwyn
- [Update validate_hacs.yaml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/0524a7cf284dbc20c9119a25704984ec72dacf61) - @RogerSelwyn
- [Update validate_hassfest.yaml](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/e895c77f9df2bb5213b739ba99a96322a9e6f0b5) - @RogerSelwyn
- [Update manifest.json](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/3f02beb53cbf020ae44d337e120769dbea60b41e) - @RogerSelwyn
- [Add numpy as requirement](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/18ee4bce536f0d2add0b0c0a84708a29e61b7631) - @RogerSelwyn
- [Keep in line with mqtt_statestream](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/706fb779e64f84e588698c6e96bdc925ac54ffb7) - @RogerSelwyn
- [Bump to v0.10.7](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/33e5ace19f85a3cdcbc1047cbde084d4ed77db75) - @RogerSelwyn
- [Auto update requirements.txt](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/530e4e41ad96d064ff1b3dd197068fe59198fa39) - @actions-user
- [Auto update manifest.json](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/399698cc9910a4bd9fa44c279dc10e2496908aeb) - @actions-user

## 0.10.6 (2023/01/05)
### Enhancements
- [Added the ability to break out commands into a separate topic structure](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/2f10f38c933d11338e93f39624687d86e5a4af91) - @RogerSelwyn
- [Add temperature step, default 0.5](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/672773a476dc538d9658d0db6c156061501d2991) - @RogerSelwyn
### Maintenance
- [Update CHANGELOG.md](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/fa7c671073cba4d511bc6bcf1beed5b3fe76bd91) - @RogerSelwyn
- [Bump to v0.10.6](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/9202ab59de10cf99c6db82891f789b172441c4e2) - @RogerSelwyn

## 0.10.5 (2023/01/04)
### Enhancements
- [Add mode/preset/temperature setting](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/71b967e2674fee43c99e135ad4424abac5dd3d7f) - @RogerSelwyn

### Maintenance
- [Segregate code to add clarity for adding climate](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/5a274b97c6b657f3be627f76d96f8a507996214f) - @RogerSelwyn
- [Bump to v0.10.5](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/bfa53600f170c347eaa5be201ea0b2637c932bd8) - @RogerSelwyn

## 0.10.4 (2023/01/04)
### Enhancements
- [Support friendly name](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/18cf6f1a94f5f72bb0e7b8dfbe0cc93c45e190ec) - @RogerSelwyn

### Maintenance
- [Convert strings to constants](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/eb83759ce944516aea33c3fd5d22c27859eae72f) - @RogerSelwyn
- [Bump to v0.10.4](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/0941c09b772a53c8a78de05b0d2d89d3a07a557c) - @RogerSelwyn

## 0.10.3 (2023/01/03)
### Maintenance
- [Code improvements](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/b7352e7338402148caabe7c07689ed99ab65e025) - @RogerSelwyn
- [Bump to v0.10.3](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/a9c439158bbb256197a7aa00c897693c7e84fc17) - @RogerSelwyn

## 0.10.2 (2022/12/29)
### Fixes
- [Fix subscription failure - retry in 10 seconds](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/53baa29c4e89673561c04c3a6dcdafab0ecb3d0b) - @RogerSelwyn

### Maintenance
- [Bring more in line with core statestream](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/edd54ec94f3aa846c533b491012568c0dba2d888) - @RogerSelwyn
- [Bump to 0.10.2](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8943750da9e2e67457b1e31c8aa56a2aa03f705f) - @RogerSelwyn


## 0.10.1 (2022/12/28)
### Enhancements
- [Add icon as standard attribute](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/ae08fef9626c01c90b2fa61c59ced97750f354f0) - @RogerSelwyn

### Maintenance
- [Substantial re-organisation of code](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/8c1407ef6fbc8f6a6b1bcab72b0748260c116333) - @RogerSelwyn
- [Bump to  0.10.1](https://github.com/RogerSelwyn/mqtt_discoverystream_ha/commit/b19bc0d4ecb7a1c4c1806d5521e692a2a34abb5a) - @RogerSelwyn

## 0.10.0 (2022/12/24)
### Enhancements
- Added climate entity support

### Maintenance
- Workaround for MQTT failure at startup

## 0.9

- Fix `async_get_registry` warning

## 0.8

- Add "discovery_topic" to split config and state topics

## 0.7

- Fix availability for lights

## 0.6

- Adapt to 2021.12

## 0.5

- Add device support
- Fix color support
- Add availability support

## 0.4

- Add device_tracker
- Add light transitions
- Initial HACS release

## 0.3

- Manage color temperature

## 0.2

- Fix binary_sensors

## 0.1

- Initial release:
  Handles:
    - sensors
    - switches
    - lights (partial)
