# Design Spec: 1-Hour BA-kit Credibility Seminar

## 1. Design Summary

This seminar should not present BA-kit as "a cool AI tool demo."

It should present a credible BA method first, then use BA-kit outputs as proof that the method can be executed in a structured, repeatable way with AI.

The goal is to build trust with:

- future or junior BAs who need a clear working model
- practicing IT BAs or PMs who need evidence of rigor, not prompt tricks

The seminar is capped at 1 hour, so a full live walkthrough of BA-kit is not the center of the session.

## 2. Audience And Conversion Goal

Primary audience:

- future or junior BAs
- working IT BAs or PMs

Primary conversion goal:

- build credibility first
- upsell `KHÓA HỌC BA AI WITH ANTIGRAVITY GOOGLE (BAAG)` as the logical next step
- position the course around doubling BA productivity by using AI Agents to reduce repetitive BA work

The audience should leave believing:

- the speaker understands real BA work
- AI can support BA work only when the process is structured
- BAAG teaches the method and hands-on AI Agent workflow behind the outputs, not just tool usage

## 3. Recommended Positioning

Recommended seminar title:

`Ứng dụng AI trong phân tích nghiệp vụ IT: Từ yêu cầu thô đến tài liệu bàn giao có thể sử dụng`

Core message:

- BA-kit is evidence
- the method is the product
- the course is the path to learn that method properly

Position BA-kit as:

- a BA workstation
- a structured lifecycle from intake to handoff
- a way to make BA work more consistent, traceable, and stakeholder-ready

Brand frame:

- The deck must use the AG Academy brand kit from `C:\Users\DPC\Downloads\AG_Academy_Brand_Kit\AG_Academy_Brand_Kit`.
- Treat AG Academy as the course brand and BA-kit as the method/evidence inside the seminar.
- Use the AG Academy slogan where useful: `Nâng tầm năng suất. Tận hưởng cuộc sống.`

Do not position BA-kit as:

- a replacement for BA thinking
- a generic AI prompting shortcut
- a long live-demo centerpiece

## 4. Recommended Session Structure

Target duration:

- 50 to 60 minutes total

Recommended time split:

1. BA pain in real projects - 5 minutes
2. What good BA work should produce - 5 minutes
3. A practical BA workflow AI should support - 10 minutes
4. How BA-kit operationalizes that workflow - 10 minutes
5. Mini proof walkthrough using real outputs - 10 to 15 minutes
6. What BA capability still matters in the AI era - 10 minutes
7. BAAG course close and CTA - 5 to 7 minutes

This structure teaches first, proves second, sells last.

## 5. BA-kit Evidence Strategy

Use BA-kit as proof, not as the full content of the seminar.

Recommended evidence set:

- `PROJECT-HOME.md` to show guided workflow and project state
- `backbone.md` to show scope lock and single source of truth
- one downstream artifact such as `user-stories.md` or `srs.md` to show traceable output quality

If visuals are needed, use screenshots or prepared excerpts of actual BA-kit output.

Avoid:

- a full cold live run from raw input to final package
- deep command walkthroughs
- explaining repo internals, agent roles, or installation details to this audience

Reason:

- full demos consume too much time
- live runs increase risk
- credibility comes from structured outputs and clear reasoning, not from runtime novelty

## 6. Slide Outline

Deck should use formal Vietnamese on slides.

Allowed English terms only where they are already standard or hard to replace cleanly:

- BA
- AI
- IT
- `PROJECT-HOME.md`
- `backbone.md`
- `SRS`

Recommended 13-slide deck with detailed direction:

### Slide 1 - `BA trong thời đại AI: Từ yêu cầu thô đến tài liệu bàn giao có thể sử dụng`

Main purpose:

- establish the promise of the seminar
- frame the session as a practical BA discussion, not a tool show

On-slide content:

- title
- subtitle: `Một phương pháp làm BA có cấu trúc, có thể áp dụng cùng AI`
- speaker name and role
- one-line promise: `Sau buổi này, anh/chị sẽ thấy rõ AI chỉ tạo ra giá trị khi BA có phương pháp đúng`

Suggested visual:

- clean hero visual showing a flow from `yêu cầu thô` to `tài liệu bàn giao`
- either a simple horizontal process diagram or a polished document transformation visual
- include AG Academy logo as a restrained title-slide brand mark:
- use `logos/01_logo_full_color.png` on a light title slide, or `logos/02_logo_white_on_dark.png` on a dark title slide

Speaker notes:

- open by setting expectation that this is not a buổi giới thiệu công cụ đơn thuần
- state that the session is about how BA can keep rigor while using AI
- explain that a real tool will appear later only as evidence for the method

### Slide 2 - `Vì sao công việc BA thường bị đứt gãy trong dự án thực tế`

Main purpose:

- make the audience agree with the problem before introducing the method

On-slide content:

- 4 to 5 failure patterns:
- `Đầu vào mơ hồ, nhiều nguồn, khó xác định phạm vi`
- `Tài liệu không thống nhất giữa các giai đoạn`
- `Thiếu truy vết từ nhu cầu đến giải pháp và kiểm thử`
- `BA mất nhiều thời gian viết lại cùng một loại tài liệu`
- `Khi dùng AI tự do, đầu ra nhanh nhưng thiếu kiểm soát chất lượng`

Suggested visual:

- a broken workflow diagram with red breakpoints between requirement, analysis, documentation, and handoff
- or a cluttered desk/document collage representing fragmented BA work

Speaker notes:

- speak from project reality, not theory
- mention that many teams do have templates and tools, but still lack a stable operating method
- connect the problem directly to audience pain: rework, misunderstandings, slow handoff, and stakeholder mistrust

### Slide 3 - `Các bên liên quan thực sự cần gì từ một BA`

Main purpose:

- shift the focus from "BA writes documents" to "BA creates decision quality"

On-slide content:

- 4 stakeholder expectations:
- `Hiểu đúng vấn đề kinh doanh`
- `Khóa phạm vi đủ rõ trước khi đi sâu`
- `Tạo tài liệu có thể bàn giao cho đội triển khai`
- `Giữ được truy vết giữa yêu cầu, giải pháp và kiểm thử`

- closing line:
- `Giá trị của BA không nằm ở số lượng tài liệu, mà nằm ở độ rõ ràng và khả năng bàn giao`

Suggested visual:

- one central BA node connected to business, product, engineering, and testing
- each connection labeled with an expected outcome

Speaker notes:

- emphasize that stakeholders do not pay for document volume
- they pay for clarity, reduced risk, and smoother execution
- this creates the bridge to the workflow slide that follows

### Slide 4 - `Một quy trình BA đơn giản nhưng đủ chặt chẽ`

Main purpose:

- teach the core method the course will later sell

On-slide content:

- 4-step flow:
- `Tiếp nhận và chuẩn hóa đầu vào`
- `Khóa phạm vi và tạo nguồn sự thật thống nhất`
- `Sinh các tài liệu phù hợp với mục tiêu bàn giao`
- `Bàn giao, rà soát, và cập nhật theo phản hồi`

- under the flow, add examples:
- `Đầu vào: brief, ghi chú họp, tài liệu yêu cầu`
- `Nguồn sự thật: backbone`
- `Tài liệu: user stories, FRD, SRS, đặc tả màn hình`

Suggested visual:

- a clean left-to-right workflow with four stages
- each stage should have one icon and one short label

Speaker notes:

- spend time here because this is the intellectual core of the seminar
- explain that AI should support this sequence, not replace it
- mention that most AI disappointment comes from skipping the scope-lock step

### Slide 5 - `Vì sao AI thường thất bại khi không có cấu trúc BA`

Main purpose:

- explain why prompting alone is insufficient

On-slide content:

- two-column comparison:
- left column `Dùng AI không có phương pháp`
- right column `Dùng AI trong quy trình BA có cấu trúc`

- comparison points:
- `Đầu vào`
- `Cách ra quyết định`
- `Độ ổn định của tài liệu`
- `Khả năng truy vết`
- `Mức độ tin cậy khi bàn giao`

Suggested visual:

- side-by-side comparison table
- optional subtle color coding: left weaker, right stronger

Speaker notes:

- this slide is important for credibility with experienced attendees
- avoid saying AI is bad; say uncontrolled usage creates weak outputs
- the goal is to position method as the multiplier of AI value

### Slide 6 - `BA-kit là gì và vai trò của nó trong quy trình này`

Main purpose:

- introduce BA-kit without turning the session into a product pitch

On-slide content:

- definition:
- `BA-kit là một bộ công cụ giúp vận hành quy trình BA có cấu trúc cùng AI`

- 3 supporting points:
- `Chuẩn hóa vòng đời làm BA từ đầu vào đến bàn giao`
- `Tạo ra các tài liệu theo logic nhất quán`
- `Giữ được trạng thái dự án, phạm vi, và bước tiếp theo`

- boundary statement:
- `BA-kit không thay thế tư duy BA; BA-kit giúp tư duy BA được vận hành nhất quán`

Suggested visual:

- one centered box `BA-kit` placed over the workflow from slide 4
- arrows showing BA-kit supporting each step

Speaker notes:

- keep this short and controlled
- do not explain installation, command surface, or internal architecture
- position BA-kit as an operating layer for BA work with AI

### Slide 7 - `Ví dụ đầu ra 1: Bảng điều phối công việc BA`

Main purpose:

- show that the process is navigable and not dependent on remembering prompts

On-slide content:

- slide title in Vietnamese
- mention the artifact by name: `PROJECT-HOME.md`
- 3 things the audience should notice:
- `Dự án đang ở trạng thái nào`
- `Bước tiếp theo là gì`
- `Những câu hỏi nào còn cần chốt`

- one bottom-line sentence:
- `Điểm mạnh ở đây là khả năng điều hướng công việc, không chỉ là khả năng sinh tài liệu`

Suggested visual:

- screenshot of a real or sanitized `PROJECT-HOME.md`
- highlight 3 areas with callout boxes:
- current status
- next step
- open questions

Speaker notes:

- tell the audience this is one of the strongest signals of maturity
- many AI workflows can generate text, but few can preserve working state cleanly
- explain why this matters for solo BA and for collaboration

### Slide 8 - `Ví dụ đầu ra 2: Tài liệu khóa phạm vi và nguồn sự thật thống nhất`

Main purpose:

- demonstrate rigor and source-of-truth discipline

On-slide content:

- artifact name: `backbone.md`
- 3 concepts to explain:
- `Phạm vi đã được chốt như thế nào`
- `Giả định và khoảng trống được ghi nhận ra sao`
- `Vì sao tài liệu này trở thành nền tảng cho các tài liệu phía sau`

- closing line:
- `Nếu không có bước này, AI chỉ đang viết nhanh hơn chứ không phân tích tốt hơn`

Suggested visual:

- screenshot or formatted excerpt of a real `backbone.md`
- highlight sections such as scope, assumptions, decisions, and unresolved items

Speaker notes:

- this is where you establish serious BA credibility
- explain that a controlled source of truth reduces downstream inconsistency
- connect to stakeholder trust and reduced rework

### Slide 9 - `Ví dụ đầu ra 3: Từ phạm vi đến tài liệu có thể bàn giao`

Main purpose:

- prove that structured upstream thinking leads to usable downstream outputs

On-slide content:

- choose one artifact only for focus:
- option A `user stories`
- option B `SRS`

- recommended choice for this audience:
- `user stories` if the room is more beginner-heavy
- `SRS` if the room is more practitioner-heavy

- show 3 quality signals:
- `Có logic xuất phát từ phạm vi đã khóa`
- `Có mức độ chi tiết phù hợp cho bàn giao`
- `Có thể dùng để trao đổi với đội triển khai hoặc kiểm thử`

Suggested visual:

- screenshot of a real artifact excerpt
- use annotation boxes to point at acceptance criteria, functional detail, or traceability cues

Speaker notes:

- do not overwhelm with too much text
- explain what makes the output usable, not merely well-formatted
- if needed, briefly compare this with a generic AI-generated document to make the difference obvious

### Slide 10 - `Những gì ví dụ này thực sự chứng minh`

Main purpose:

- translate the artifact examples into business credibility

On-slide content:

- 4 proof points:
- `AI có thể hỗ trợ BA nhanh hơn`
- `Nhưng chất lượng chỉ ổn định khi quy trình được thiết kế đúng`
- `Đầu ra có thể nhất quán giữa các giai đoạn`
- `BA vẫn là người chịu trách nhiệm về tư duy và quyết định`

Suggested visual:

- a simple synthesis diagram linking `Phương pháp` + `AI` + `Công cụ` -> `Đầu ra đáng tin cậy`

Speaker notes:

- this slide prevents the audience from remembering only the screenshots
- restate that the seminar is about operating model credibility
- make the lesson explicit: tool value comes from method discipline

### Slide 11 - `Trong thời đại AI, BA cần học gì để không bị thay thế`

Main purpose:

- create demand for the course without pitching too early

On-slide content:

- 4 capability areas:
- `Tư duy phân tích và làm rõ yêu cầu`
- `Khả năng khóa phạm vi và quản lý quyết định`
- `Khả năng tạo tài liệu có thể bàn giao`
- `Khả năng sử dụng AI như một công cụ có kiểm soát`

- one closing sentence:
- `Người bị thay thế không phải là BA dùng ít AI, mà là BA dùng AI nhưng thiếu phương pháp`

Suggested visual:

- four-pillar capability model
- each pillar labeled with one competency area

Speaker notes:

- this is the transition slide into the upsell
- keep the tone educational, not threatening
- emphasize augmentation and professional maturity

### Slide 12 - `Khóa học BA AI with Antigravity Google: Gấp đôi năng suất BA`

Main purpose:

- introduce the course offer as the direct answer to the pain points from the seminar
- make the productivity promise concrete without sounding like a generic AI hype pitch

On-slide content:

- course name:
- `KHÓA HỌC BA AI WITH ANTIGRAVITY GOOGLE`

- headline promise:
- `Gấp đôi năng suất BA, giảm mạnh công việc lặp lại`

- pain hook:
- `Bạn vẫn đang mất 2–3 ngày để viết SRS, hàng giờ để vẽ ERD, viết test case thủ công?`

- pivot line:
- `Đã đến lúc làm BA theo cách của AI Agent.`

- 3 proof-oriented outcomes:
- `Viết SRS từ brief thô trong 45 phút thay vì 3 ngày`
- `Generate ERD + API Spec chỉ với 1 prompt`
- `Tạo 50+ test cases từ SRS trong 5 phút`

Suggested visual:

- strong course offer slide with one large promise, one pain statement, and three result chips
- optional Antigravity Google / AI Agent visual cue
- use AG Academy brand colors: AG Purple `#7c3aed`, AG Cyan `#06b6d4`, Dark Navy `#1a1a2e`
- use `logos/02_logo_white_on_dark.png` if the slide uses a dark navy background
- avoid cramming every artifact name here; reserve detailed artifact list for Slide 13

Speaker notes:

- acknowledge the audience's current manual workload directly
- make the promise specific: faster SRS, faster ERD/API Spec, faster test cases
- emphasize that speed comes from structured BA thinking plus AI Agent workflow
- avoid promising that AI replaces BA judgment

### Slide 13 - `Sau khóa học BAAG, anh/chị có thể tạo bộ tài liệu BA hoàn chỉnh`

Main purpose:

- close with a concrete outcome list and direct CTA
- show that BAAG is a hands-on course where learners build a real product/tool, not a theory-only class

On-slide content:

- intro line:
- `Khóa học BA ứng dụng AI (BAAG) giúp anh/chị làm được việc thật ngay tại lớp`

- build promise:
- `Build 1 sản phẩm/tool thực tế ngay tại lớp – không cần code`

- outcome block:
- `Phân tích ghi âm cuộc họp thành tài liệu hoàn chỉnh`
- `Tự động tạo BRD, SRS, ERD, API Spec và Test Cases`

- artifact checklist:
- `BRD — Business Requirements`
- `SRS — Software Requirements Specification`
- `ERD — Entity Relationship Diagram`
- `API Spec`
- `Test Cases`

- CTA:
- `Nếu anh/chị muốn học phương pháp phía sau các đầu ra vừa xem, BAAG là lộ trình thực hành để bắt đầu`

- optional footer:
- registration channel, QR code, or contact point

Suggested visual:

- outcome checklist arranged as a document pipeline from meeting recording to BA handoff pack
- one QR/contact block on the right or bottom
- use `logos/04_logo_horizontal.png` in the footer or CTA area if the layout is wide
- use `logos/03_logo_icon_only.png` as a subtle watermark only if opacity stays low and text contrast remains high
- use checkmarks sparingly; do not make the slide look like a sales flyer

Speaker notes:

- connect back to the three BA-kit evidence artifacts shown earlier
- explain that the course teaches repeatable workflow: meeting/brief input -> analysis -> artifact generation -> review
- close with a clear next action: scan QR, leave contact, or register
- keep the pitch direct but grounded in the work products the audience already understands

## 7. Visual Design Guidance For The Deck

Brand kit source:

- `C:\Users\DPC\Downloads\AG_Academy_Brand_Kit\AG_Academy_Brand_Kit`
- guideline file: `brand_guidelines.md`
- logo files:
- `logos/01_logo_full_color.png` for light slides
- `logos/02_logo_white_on_dark.png` for dark slides
- `logos/03_logo_icon_only.png` for favicon/avatar/watermark only
- `logos/04_logo_horizontal.png` for header/footer/CTA strips
- `logos/05_logo_monochrome.png` only for print-style or monochrome treatment
- mockup reference: `mockups/mockup_overview.png`

Overall style:

- formal
- business-facing
- clean and structured
- closer to consulting presentation than startup product pitch
- still visibly AG Academy, not a generic consulting deck

Typography direction:

- use Inter according to the AG Academy guideline
- Heading: Inter 700-800
- Body: Inter 400
- Slogan or soft supporting line: Inter 300-400 italic when needed
- avoid playful or overly decorative type
- keep hierarchy obvious between title, key point, and evidence

Color direction:

- primary palette must follow AG Academy:
- AG Purple `#7c3aed`
- AG Cyan `#06b6d4`
- Dark Navy `#1a1a2e`
- Light Gray `#f5f5f8`
- Muted `#8888a0`
- White `#ffffff`
- use the AG gradient only for controlled emphasis: `linear-gradient(135deg, #7c3aed, #06b6d4)`
- avoid making every slide a purple/cyan gradient; use dark navy, light gray, and white to keep the seminar credible

Image rules:

- use screenshots of real BA-kit outputs when possible
- crop tightly and annotate intentionally
- every screenshot must support one message only
- logo usage must follow AG Academy rules:
- preserve aspect ratio
- do not recolor, rotate, distort, add glow, shadow, or outline to the logo
- keep clear space around the logo
- do not place logo directly on a complex image; add a clean overlay or use a solid header/footer area

Layout rules:

- avoid text-heavy slides
- one core idea per slide
- when a screenshot appears, reduce text and let annotations carry the explanation
- keep AG Academy logo at a consistent size and position across repeated slide types
- title slide and final CTA slides can be more brand-forward; method/evidence slides should use lighter branding so the content stays credible

## 8. Speaker Guidance

Tone:

- practical
- method-first
- not overhyped

Messaging rules:

- teach a reusable BA way of thinking
- use BA-kit to validate that the method can be operationalized
- keep "AI" attached to process quality, not magic

Useful line of argument:

- bad input plus loose prompting creates weak BA output
- structured intake and backbone thinking create better output
- BA-kit is credible because it enforces that structure

## 9. Course Upsell Logic

The course offer should feel like the natural continuation of the seminar.

The seminar proves:

- what good BA work looks like
- how AI can accelerate it responsibly
- why prompting alone is insufficient

The course to upsell is:

- `KHÓA HỌC BA AI WITH ANTIGRAVITY GOOGLE`
- short name: `BAAG`
- positioning line: `Gấp đôi năng suất BA, hỗ trợ công việc lặp lại`

The course should then promise practical outcomes:

- write SRS from a rough brief in about 45 minutes instead of 2-3 days
- generate ERD and API Spec from a structured prompt/workflow
- create 50+ test cases from an SRS in minutes
- build one real product/tool in class without needing to code
- analyze meeting recordings into a complete BA documentation pack
- automatically produce BRD, SRS, ERD, API Spec, and Test Cases

The CTA should be soft:

- "If you want to learn the method behind these outputs, BAAG is the hands-on path to practice it."

Messaging guardrails:

- do not pitch BAAG as "one prompt replaces BA work"
- do not overpromise perfect documents without BA review
- frame Antigravity Google as the AI Agent workspace that helps BA execute repeated work faster
- keep the claim tied to structured inputs, BA review, and repeatable workflow

## 10. Constraints And Risks

Constraints:

- maximum 1 hour
- mixed audience from beginner to practitioner
- no direct hard-sell framing

Risks:

- too much demo reduces teaching value
- too much theory makes BA-kit feel unproven
- too much product talk weakens credibility

Mitigation:

- show only 3 concrete BA-kit outputs
- keep the workflow visual simple
- reserve the last 5 to 7 minutes for the BAAG course pitch

## 11. Success Criteria

The seminar succeeds if attendees can clearly say:

- "I understand the BA workflow better now."
- "This speaker has a serious BA method, not just AI tricks."
- "The tool outputs look practical and usable."
- "The course seems worth considering if I want to learn this properly."
