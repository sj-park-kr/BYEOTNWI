# 로고

최종: **A안 THE GAP v3** — 두 N 사이 틈으로 햇볕이 새어 드는 워드마크.

| 파일 | 용도 |
|---|---|
| `byeonnwi_a_gap_v3.svg` / `byeonnwi_main_v3.png` | 메인(어두운 배경, 1600x560) |
| `byeonnwi_a_gap_light_v3.svg` / `.png` | 밝은 배경 |
| `byeonnwi_detail_v3.png` | 틈 부분 3배 확대 |
| `*_v2`, v1(`byeonnwi_main.png`, `byeonnwi_concepts.png`, `b_slice`, `c_sunfleck`) | 이전 시안 |

SVG는 글자를 패스로 변환해 폰트 없이 동일하게 보임.

## 컬러
| 용도 | HEX |
|---|---|
| 배경 | `#0B0A09` |
| 글자 | `#F2EBDD` |
| 앰버 | `#FF9F1C` |
| 골드 | `#FFC93C` |
| 빛 코어 | `#FFF1C1` |
| 밝은 배경 / 글자 | `#F4EEE3` / `#15120F` |

## 폰트 (OFL, Google Fonts)
Anton(워드마크), Noto Sans KR 800(한글 태그라인), Archivo Black·Bebas Neue(이전 시안). `fonts/`에 포함.

## 재생성
```bash
cd logo/src
pip install fonttools brotli
python gen_v3.py      # SVG 생성 (gen.py 임포트 시 v1 시안도 다시 씀)
node render_v3.js     # PNG 렌더 (playwright 필요)
```
