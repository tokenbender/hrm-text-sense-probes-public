# Diagnostics: vibe-2026-expanded-120-harness-20260519T095252Z

- Outputs: `1320`
- Errors: `0`
- Scope: mechanical red flags only, not a correctness score.

## Model Red Flags

| Model | Avg tokens | Flags |
|---|---:|---|
| `hrm_direct` | 17.2 | repeated_line: 1, special_token_leak: 120, too_terse: 58 |
| `smollm2_instruct` | 76.4 | hit_token_cap: 4, prompt_echo: 10, special_token_leak: 118, too_terse: 2 |
| `qwen25_05b_instruct` | 146.6 | hit_token_cap: 40, prompt_echo: 3, special_token_leak: 80, too_terse: 2 |
| `h2o_danube3_500m_chat` | 107.7 | hit_token_cap: 28, prompt_echo: 17, repeated_line: 6, special_token_leak: 92 |
| `falcon3_1b_instruct` | 124.5 | hit_token_cap: 35, prompt_echo: 4, repeated_line: 3, special_token_leak: 85, too_terse: 4 |
| `tinyllama_11b_chat` | 83.9 | hit_token_cap: 8, prompt_echo: 8, repeated_line: 1, special_token_leak: 112 |
| `lfm25_12b_instruct` | 135.9 | hit_token_cap: 24, prompt_echo: 5, special_token_leak: 97, too_terse: 2 |
| `qwen25_15b_instruct` | 131.8 | hit_token_cap: 27, prompt_echo: 2, special_token_leak: 94, too_terse: 3 |
| `qwen3_06b_thinking` | 250.5 | hit_token_cap: 111, prompt_echo: 4, special_token_leak: 9, unfinished_thinking: 103 |
| `qwen3_17b_thinking` | 254.3 | hit_token_cap: 117, special_token_leak: 3, unfinished_thinking: 115 |
| `h2o_danube2_18b_chat` | 149.4 | hit_token_cap: 25, prompt_echo: 2, special_token_leak: 95 |

## Category Red Flags

| Category | Flags |
|---|---|
| `ambiguity` | hit_token_cap: 38, prompt_echo: 1, repeated_line: 3, special_token_leak: 72, unfinished_thinking: 19 |
| `causal_sense` | hit_token_cap: 70, prompt_echo: 1, special_token_leak: 42, too_terse: 6, unfinished_thinking: 20 |
| `compression` | hit_token_cap: 22, prompt_echo: 31, repeated_line: 2, special_token_leak: 88, too_terse: 4, unfinished_thinking: 19 |
| `contradiction_detection` | hit_token_cap: 53, prompt_echo: 3, repeated_line: 2, special_token_leak: 57, too_terse: 2, unfinished_thinking: 20 |
| `epistemic_restraint` | hit_token_cap: 54, prompt_echo: 4, special_token_leak: 57, too_terse: 6, unfinished_thinking: 19 |
| `instruction_boundaries` | hit_token_cap: 57, prompt_echo: 3, special_token_leak: 54, too_terse: 7, unfinished_thinking: 20 |
| `negation` | hit_token_cap: 22, prompt_echo: 3, repeated_line: 1, special_token_leak: 88, too_terse: 11, unfinished_thinking: 18 |
| `reference_resolution` | hit_token_cap: 21, special_token_leak: 89, too_terse: 7, unfinished_thinking: 20 |
| `state_tracking` | hit_token_cap: 22, prompt_echo: 6, special_token_leak: 88, too_terse: 3, unfinished_thinking: 19 |
| `stop_condition` | hit_token_cap: 18, special_token_leak: 92, too_terse: 21, unfinished_thinking: 15 |
| `style_control` | hit_token_cap: 16, prompt_echo: 1, repeated_line: 2, special_token_leak: 94, unfinished_thinking: 11 |
| `update_handling` | hit_token_cap: 26, prompt_echo: 2, repeated_line: 1, special_token_leak: 84, too_terse: 4, unfinished_thinking: 18 |

## Flagged Examples

### `exp_state_01` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Clipboard Drawer Swap
- Output tokens: `22`

```text
The silver clipboard is in the left drawer and Teo added a yellow folder.<|box_end|>
```

### `exp_state_02` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Plant Tray Key
- Output tokens: `24`

```text
The brass key is on the shelf, and a receipt is on the tray.<|box_end|>
```

### `exp_state_03` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Blue Tape Roll
- Output tokens: `27`

```text
The tape is in the tall bin, and the marker is in the small bin.<|box_end|>
```

### `exp_state_04` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Cart Handle Tag
- Output tokens: `14`

```text
Handle 4: Red tag
Car: Bay 2<|box_end|>
```

### `exp_state_05` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Notebook Under Scale
- Output tokens: `24`

```text
The notebook is on the counter and the timer is in the scale.<|box_end|>
```

### `exp_state_06` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Mug Shelf Cloth
- Output tokens: `6`

```text
Black mug and white cup<|box_end|>
```

### `exp_state_07` / `hrm_direct` / special_token_leak, too_terse

- Category: `state_tracking`
- Title: Ticket Envelope
- Output tokens: `4`

```text
inbox<|box_end|>
```

### `exp_state_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `state_tracking`
- Title: Cable Hook
- Output tokens: `3`

```text
headphones<|box_end|>
```

### `exp_state_09` / `hrm_direct` / special_token_leak

- Category: `state_tracking`
- Title: Crate Mat
- Output tokens: `24`

```text
The crate is on the floor and the mat is under the crate.<|box_end|>
```

### `exp_state_10` / `hrm_direct` / special_token_leak, too_terse

- Category: `state_tracking`
- Title: Folder in Basket
- Output tokens: `4`

```text
archive wall<|box_end|>
```

### `exp_update_01` / `hrm_direct` / special_token_leak

- Category: `update_handling`
- Title: Pickup Window Correction
- Output tokens: `41`

```text
Rafi will pick up the samples at 4:00 and return the cooler.
Mina will return the cooler at 4:10.<|box_end|>
```

### `exp_update_02` / `hrm_direct` / special_token_leak, too_terse

- Category: `update_handling`
- Title: Poster Approval Revision
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_update_03` / `hrm_direct` / special_token_leak

- Category: `update_handling`
- Title: Badge Count Update
- Output tokens: `9`

```text
9 ready badges and 1 cracked badge<|box_end|>
```

### `exp_update_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `update_handling`
- Title: Courier Name Change
- Output tokens: `3`

```text
Bela<|box_end|>
```

### `exp_update_05` / `hrm_direct` / special_token_leak

- Category: `update_handling`
- Title: Room Setup Edit
- Output tokens: `16`

```text
Room E: Projector
Room F: 4 stools<|box_end|>
```

### `exp_update_06` / `hrm_direct` / special_token_leak

- Category: `update_handling`
- Title: Menu Allergen Correction
- Output tokens: `18`

```text
The walnut tart contains walnuts; only the lemon bar is nut-free.<|box_end|>
```

### `exp_update_07` / `hrm_direct` / special_token_leak

- Category: `update_handling`
- Title: Shipment Hold Change
- Output tokens: `16`

```text
Vera: Held for seal check
MOSS: Cleared<|box_end|>
```

### `exp_update_08` / `hrm_direct` / special_token_leak

- Category: `update_handling`
- Title: Volunteer Time Revision
- Output tokens: `17`

```text
Amaya: 10 to noon
Luis: 9 to noon<|box_end|>
```

### `exp_update_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `update_handling`
- Title: Invoice Recipient Update
- Output tokens: `3`

```text
Mira<|box_end|>
```

### `exp_update_10` / `hrm_direct` / special_token_leak, too_terse

- Category: `update_handling`
- Title: Key Location Revision
- Output tokens: `4`

```text
The desk cup<|box_end|>
```

### `exp_boundary_01` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Quoted Refund Demand
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_boundary_02` / `hrm_direct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Poster Text Command
- Output tokens: `46`

```text
The coordinator should call the production team to discuss the issue. If the production team does not agree, they can request a safety review from the relevant regulatory agency.<|box_end|>
```

### `exp_boundary_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Label Says Override
- Output tokens: `2`

```text
B<|box_end|>
```

### `exp_boundary_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Voice Memo Quote
- Output tokens: `2`

```text
No<|box_end|>
```

### `exp_boundary_05` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Form Example Trap
- Output tokens: `8`

```text
Reject the order<|box_end|>
```

### `exp_boundary_06` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Email Forwarded Line
- Output tokens: `8`

```text
Reject the tiles<|box_end|>
```

### `exp_boundary_07` / `hrm_direct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Package Insert
- Output tokens: `9`

```text
Replace the blender.<|box_end|>
```

### `exp_boundary_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Meeting Transcript
- Output tokens: `2`

```text
No<|box_end|>
```

### `exp_boundary_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `instruction_boundaries`
- Title: Ticket Body Override
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_boundary_10` / `hrm_direct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Recipe Card Command
- Output tokens: `19`

```text
The prep leader should ignore the allergy stickers and continue using batch SAGE.<|box_end|>
```

### `exp_cause_01` / `hrm_direct` / special_token_leak

- Category: `causal_sense`
- Title: Scanner Cold Start
- Output tokens: `26`

```text
The scanner is malfunctioning and the bad card is a result of the scanner malfunctioning.<|box_end|>
```

### `exp_cause_02` / `hrm_direct` / special_token_leak, too_terse

- Category: `causal_sense`
- Title: Kettle Outlet
- Output tokens: `4`

```text
concurrent failure<|box_end|>
```

### `exp_cause_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `causal_sense`
- Title: Door Alarm Rain
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_cause_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `causal_sense`
- Title: Printer Color Streak
- Output tokens: `4`

```text
startup residue<|box_end|>
```

### `exp_cause_05` / `hrm_direct` / special_token_leak

- Category: `causal_sense`
- Title: Freezer Beep
- Output tokens: `15`

```text
The freezer door is broken or the thermostat is broken.<|box_end|>
```

### `exp_cause_06` / `hrm_direct` / special_token_leak, too_terse

- Category: `causal_sense`
- Title: App Slow Login
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_cause_07` / `hrm_direct` / special_token_leak, too_terse

- Category: `causal_sense`
- Title: Washer Vibration
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_cause_08` / `hrm_direct` / special_token_leak

- Category: `causal_sense`
- Title: Lamp Flicker
- Output tokens: `10`

```text
The light bulb may be on low power.<|box_end|>
```

### `exp_cause_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `causal_sense`
- Title: Scale Drift
- Output tokens: `4`

```text
Thermal expansion<|box_end|>
```

### `exp_cause_10` / `hrm_direct` / special_token_leak

- Category: `causal_sense`
- Title: Tablet Touch
- Output tokens: `9`

```text
The phone's charging port is blocked.<|box_end|>
```

### `exp_ambig_01` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Dock Note
- Output tokens: `47`

```text
1. "By the dock" can refer to the office building or the dock.
2. "By the dock" can refer to the dock area.<|box_end|>
```

### `exp_ambig_02` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Charge Slip
- Output tokens: `75`

```text
1. The charge on the item being sold is the price.
2. The charge on the item is the amount of money paid to the seller.
3. The charge before handoff means the amount paid to the seller before the item is sold.<|box_end|>
```

### `exp_ambig_03` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Press Room
- Output tokens: `57`

```text
1. Moving the press is a way to keep the guests from getting a bad impression of the company.
2. The press is a way to get the guests to know about the company.<|box_end|>
```

### `exp_ambig_04` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Light Box
- Output tokens: `32`

```text
1. A light box is a piece of equipment used to produce light.
2. The light box is a container for a light source.<|box_end|>
```

### `exp_ambig_05` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Scale Check
- Output tokens: `51`

```text
1. Check the scale of goods on the warehouse floor.
2. Check the scale of the goods on the warehouse floor before they are placed into the warehouse.<|box_end|>
```

### `exp_ambig_06` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Plant Issue
- Output tokens: `36`

```text
1. A plant is a source of food for the facility.
2. The plant is a plant that has been moved to a different location.<|box_end|>
```

### `exp_ambig_07` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: File Arm
- Output tokens: `63`

```text
1. The arm of a file unit is the physical part of the file unit that holds the data.
2. The arm of a file unit is the name of the file system that the data belongs to.<|box_end|>
```

### `exp_ambig_08` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Tag Order
- Output tokens: `55`

```text
1. Clear the tag to show that it is not for sale.
2. Clear the tag to indicate that it is for use by the customer.

Question: What does the first meaning mean in this context?<|box_end|>
```

### `exp_ambig_09` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Seal Desk
- Output tokens: `29`

```text
1. The seal is missing from the office cabinet.
2. The seal is missing from the office bag.<|box_end|>
```

### `exp_ambig_10` / `hrm_direct` / special_token_leak

- Category: `ambiguity`
- Title: Press Pass
- Output tokens: `49`

```text
1. The lobbyist is asking the press to confirm their identity and not share it with others.
2. The lobbyist is asking the press to leave the reception area until they are confirmed.<|box_end|>
```

### `exp_neg_01` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Unless Noon
- Output tokens: `2`

```text
Yes<|box_end|>
```

### `exp_neg_02` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Not Both Vans
- Output tokens: `4`

```text
Van 2<|box_end|>
```

### `exp_neg_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Only If Badge
- Output tokens: `2`

```text
No<|box_end|>
```

### `exp_neg_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Except Wet Floor
- Output tokens: `2`

```text
wet<|box_end|>
```

### `exp_neg_05` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: No Longer Hold
- Output tokens: `2`

```text
Yes<|box_end|>
```

### `exp_neg_06` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Unless Canceled
- Output tokens: `4`

```text
Room A<|box_end|>
```

### `exp_neg_07` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Not Unless Supervisor
- Output tokens: `3`

```text
No refund<|box_end|>
```

### `exp_neg_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Only One Approved
- Output tokens: `2`

```text
No<|box_end|>
```

### `exp_neg_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: If Missing Backup
- Output tokens: `2`

```text
Yes<|box_end|>
```

### `exp_neg_10` / `hrm_direct` / special_token_leak, too_terse

- Category: `negation`
- Title: Unless Late
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_epistemic_01` / `hrm_direct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Subject Says Paid
- Output tokens: `28`

```text
Known: Payment received for EBR-5.
Unknown: Payment amount.
Next check: Payment amount received.<|box_end|>
```

### `exp_epistemic_02` / `hrm_direct` / special_token_leak, too_terse

- Category: `epistemic_restraint`
- Title: Photo of Door
- Output tokens: `2`

```text
Yes<|box_end|>
```

### `exp_epistemic_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `epistemic_restraint`
- Title: Box Looks Dry
- Output tokens: `2`

```text
No<|box_end|>
```

### `exp_epistemic_04` / `hrm_direct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Calendar Invite
- Output tokens: `8`

```text
The date of signing is unknown.<|box_end|>
```

### `exp_epistemic_05` / `hrm_direct` / special_token_leak, too_terse

- Category: `epistemic_restraint`
- Title: Badge Beep Heard
- Output tokens: `2`

```text
No<|box_end|>
```

### `exp_epistemic_06` / `hrm_direct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Receipt Icon
- Output tokens: `21`

```text
The amount received from vendor Tilo is not included in the vendor's income statement.<|box_end|>
```

### `exp_epistemic_07` / `hrm_direct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Warm Box
- Output tokens: `22`

```text
The temperature of the lunch box is between 0 and 100 degrees Celsius.<|box_end|>
```

### `exp_epistemic_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `epistemic_restraint`
- Title: Forwarded Approval
- Output tokens: `3`

```text
Send<|box_end|>
```

### `exp_epistemic_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `epistemic_restraint`
- Title: Empty Shelf
- Output tokens: `2`

```text
no<|box_end|>
```

### `exp_epistemic_10` / `hrm_direct` / special_token_leak, too_terse

- Category: `epistemic_restraint`
- Title: Green Light
- Output tokens: `3`

```text
Charging<|box_end|>
```

### `exp_compress_01` / `hrm_direct` / special_token_leak

- Category: `compression`
- Title: Lab Door Rule
- Output tokens: `30`

```text
Lab B is closed after 6 p.m. Badge holders may enter later only for freezer alarms. Visitors are never allowed after 6.<|box_end|>
```

### `exp_compress_02` / `hrm_direct` / special_token_leak

- Category: `compression`
- Title: Bike Storage Rule
- Output tokens: `10`

```text
Bikes are not stored in lobby overnight.<|box_end|>
```

### `exp_compress_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `compression`
- Title: Printer Use Rule
- Output tokens: `2`

```text
C<|box_end|>
```

### `exp_compress_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `compression`
- Title: Kitchen Access Rule
- Output tokens: `6`

```text
BASIL-6<|box_end|>
```

### `exp_compress_05` / `hrm_direct` / special_token_leak

- Category: `compression`
- Title: Tool Cage Rule
- Output tokens: `25`

```text
```
ToolCageLocked
Locked
Emergency Repairs
Trainees
No
```<|box_end|>
```

### `exp_compress_06` / `hrm_direct` / special_token_leak, too_terse

- Category: `compression`
- Title: Archive Rule
- Output tokens: `2`

```text
C<|box_end|>
```

### `exp_compress_07` / `hrm_direct` / special_token_leak, too_terse

- Category: `compression`
- Title: Loading Gate Rule
- Output tokens: `2`

```text
C<|box_end|>
```

### `exp_compress_08` / `hrm_direct` / special_token_leak, repeated_line

- Category: `compression`
- Title: Server Room Rule
- Output tokens: `121`

```text
Date: NODE-7
Account Title: Servicer Room
Debit: $250
Account Title: Accounts Receivable
Credit: $250

Date: NODE-7
Account Title: Accounts Receivable
Debit: $125
Account Title: Sales Revenue
Credit: $125

Date: NODE-7
Account Title: Sales Revenue
Debit: $125
Account Title: Accounts Receivable
Credit: $125<|box_end|>
```

### `exp_compress_09` / `hrm_direct` / special_token_leak

- Category: `compression`
- Title: Checkout Override Rule
- Output tokens: `10`

```text
PARKING_IN_NOON<|box_end|>
```

### `exp_compress_10` / `hrm_direct` / special_token_leak

- Category: `compression`
- Title: Storage Lift Rule
- Output tokens: `40`

```text
1. Lift used during inventory period: Closed
2. Lift used for blocked exits during inventory period: Open
3. Lift used by visitors during inventory period: Closed<|box_end|>
```

### `exp_contradict_01` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Two Freezer Logs
- Output tokens: `62`

```text
Conflict: Log A claims the red freezer bag left at 8:10, while Log B claims it was still on shelf 3 at 8:25.
Safeest assumption: The red freezer bag left the shelf at 8:15.<|box_end|>
```

### `exp_contradict_02` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Badge Return Conflict
- Output tokens: `62`

```text
The conflict is between Note A and Note B. The safe next step is to contact the manager who assigned the badge to the drawer. If they are not available, the manager can contact the owner of the drawer.<|box_end|>
```

### `exp_contradict_03` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Medicine Box Notes
- Output tokens: `54`

```text
Conflict: Note A claims the medicine box was delivered to Clinic C, while Note B claims only paperwork was delivered and the medicine box remained in Cooler 1.
Safe assumption: The medicine box was delivered to Clinic C.<|box_end|>
```

### `exp_contradict_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `contradiction_detection`
- Title: Key Pickup Conflict
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_contradict_05` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Crate Scan Conflict
- Output tokens: `30`

```text
Scan B should read the crate OAK's address in bay 1 and send it to the correct location.<|box_end|>
```

### `exp_contradict_06` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Laptop Handoff Conflict
- Output tokens: `9`

```text
Jules took the laptop<|box_end|>
```

### `exp_contradict_07` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Sample Sleeve Conflict
- Output tokens: `50`

```text
Conflict: The courier note (B) and lab note (L) state different things about sample sleeve pick-up.
Safeest operational assumption: The label sheet was picked up, and the sleeve was not picked up.<|box_end|>
```

### `exp_contradict_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `contradiction_detection`
- Title: Door Repair Conflict
- Output tokens: `2`

```text
A<|box_end|>
```

### `exp_contradict_09` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Deposit Drop Conflict
- Output tokens: `42`

```text
Conflict: Cash note (Dropped) vs Bank note (Received Envelope, Safe Pouch)
Next check: Check the bank statement for any errors or missing information.<|box_end|>
```

### `exp_contradict_10` / `hrm_direct` / special_token_leak

- Category: `contradiction_detection`
- Title: Tablet Return Conflict
- Output tokens: `10`

```text
Mira has the tablet.<|box_end|>
```

### `exp_style_01` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Bakery Plain Reasons
- Output tokens: `51`

```text
1. The cafe might not have enough space in the kitchen to bake more muffins.
2. The customers might have eaten all the muffins or they might have ordered more.
3. The customers might have changed their orders.<|box_end|>
```

### `exp_style_02` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Late Bus Plain
- Output tokens: `26`

```text
1. The shuttle's engine failed.
2. The shuttle's driver forgot to check the bus stop sign.<|box_end|>
```

### `exp_style_03` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Newsletter Tone
- Output tokens: `11`

```text
"Our filing cabinet changes everything for office storage."<|box_end|>
```

### `exp_style_04` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Three Calm Fixes
- Output tokens: `40`

```text
1. Turn off the water and turn off the sink
2. Remove the trash and debris
3. Remove the clogged drain<|box_end|>
```

### `exp_style_05` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: No Theater Stockout
- Output tokens: `32`

```text
A small shop might run out of receipt paper due to a lack of paper stock or a sudden increase in the number of receipts.<|box_end|>
```

### `exp_style_06` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Plain Apology
- Output tokens: `13`

```text
I'm sorry I sent the wrong file.<|box_end|>
```

### `exp_style_07` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Mundane Delay List
- Output tokens: `51`

```text
1. The repair company doesn't sell tickets on Mondays.
2. The repair company doesn't sell tickets on Wednesdays.
3. The repair company doesn't sell tickets on Fridays.
4. The repair company doesn't sell tickets on Saturdays.<|box_end|>
```

### `exp_style_08` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Short Neutral Notice
- Output tokens: `17`

```text
The west elevator is out of service. Please call me if you need assistance.<|box_end|>
```

### `exp_style_09` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: No Praise Summary
- Output tokens: `43`

```text
1. Count the total number of units.
2. Calculate the average inventory level by dividing the total number of units by the number of units sold.<|box_end|>
```

### `exp_style_10` / `hrm_direct` / special_token_leak

- Category: `style_control`
- Title: Exact Format Hours
- Output tokens: `11`

```text
Open: 9; Closed: 5<|box_end|>
```

### `exp_ref_01` / `hrm_direct` / special_token_leak

- Category: `reference_resolution`
- Title: Apron Swap
- Output tokens: `12`

```text
Omar's apron; Lena's old apron<|box_end|>
```

### `exp_ref_02` / `hrm_direct` / special_token_leak

- Category: `reference_resolution`
- Title: Key Card Handback
- Output tokens: `21`

```text
Theo has the guest key card and Jules returned the expired card.<|box_end|>
```

### `exp_ref_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `reference_resolution`
- Title: Notebook Borrow
- Output tokens: `3`

```text
Rafi<|box_end|>
```

### `exp_ref_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `reference_resolution`
- Title: Badge Clip
- Output tokens: `3`

```text
Bo's<|box_end|>
```

### `exp_ref_05` / `hrm_direct` / special_token_leak, too_terse

- Category: `reference_resolution`
- Title: Umbrella Loan
- Output tokens: `2`

```text
blue<|box_end|>
```

### `exp_ref_06` / `hrm_direct` / special_token_leak

- Category: `reference_resolution`
- Title: Tablet Case
- Output tokens: `19`

```text
Mara is using Kei's case. Lio discarded Kei's old case.<|box_end|>
```

### `exp_ref_07` / `hrm_direct` / special_token_leak, too_terse

- Category: `reference_resolution`
- Title: Locker Token
- Output tokens: `3`

```text
Sam's<|box_end|>
```

### `exp_ref_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `reference_resolution`
- Title: Clipboard Trade
- Output tokens: `4`

```text
Uma's<|box_end|>
```

### `exp_ref_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `reference_resolution`
- Title: Scanner Loan
- Output tokens: `4`

```text
Oren's<|box_end|>
```

### `exp_ref_10` / `hrm_direct` / special_token_leak

- Category: `reference_resolution`
- Title: Coat Mix
- Output tokens: `20`

```text
Kai wears the raincoat, and Lin hung the winter coat.<|box_end|>
```

### `exp_stop_01` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Missing Stapler
- Output tokens: `4`

```text
Shelf B<|box_end|>
```

### `exp_stop_02` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Find First Unlocked
- Output tokens: `5`

```text
Door 2<|box_end|>
```

### `exp_stop_03` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Tray Without Map
- Output tokens: `2`

```text
blue<|box_end|>
```

### `exp_stop_04` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Expired Badge
- Output tokens: `2`

```text
B<|box_end|>
```

### `exp_stop_05` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Missing Screw
- Output tokens: `5`

```text
Kit 2<|box_end|>
```

### `exp_stop_06` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Earliest Open Slot
- Output tokens: `3`

```text
10<|box_end|>
```

### `exp_stop_07` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Find Mismatch
- Output tokens: `3`

```text
box B<|box_end|>
```

### `exp_stop_08` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: First Dry Towel
- Output tokens: `6`

```text
Towel 2<|box_end|>
```

### `exp_stop_09` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Missing Charger
- Output tokens: `2`

```text
south<|box_end|>
```

### `exp_stop_10` / `hrm_direct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Only Failed Check
- Output tokens: `4`

```text
latch failed<|box_end|>
```

### `exp_state_01` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Clipboard Drawer Swap
- Output tokens: `28`

```text
The silver clipboard is now in the right drawer, and Teo added a yellow folder to the now-unlabeled left drawer.<|im_end|>
```

### `exp_state_02` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Plant Tray Key
- Output tokens: `18`

```text
The brass key is now on the shelf, and the receipt is on the tray.<|im_end|>
```

### `exp_state_03` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Blue Tape Roll
- Output tokens: `20`

```text
The tape is located in the small bin, and the marker is located in the small bin.<|im_end|>
```

### `exp_state_04` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `state_tracking`
- Title: Cart Handle Tag
- Output tokens: `61`

```text
Owen clipped a green tag to cart handle 4. The cart was rolled to bay 2, but only its handle cover was removed. Priya then clipped a red tag to handle 4. The green tag is on handle 4 and it is currently in bay 2.<|im_end|>
```

### `exp_state_05` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Notebook Under Scale
- Output tokens: `20`

```text
The notebook is placed under the scale, and the timer is placed on the empty scale spot.<|im_end|>
```

### `exp_state_06` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Mug Shelf Cloth
- Output tokens: `30`

```text
Based on the information provided, the black mug is now behind the folded cloth on shelf B. The cloth has been moved to shelf C.<|im_end|>
```

### `exp_state_07` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Ticket Envelope
- Output tokens: `9`

```text
The ticket is in the red envelope.<|im_end|>
```

### `exp_state_08` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Cable Hook
- Output tokens: `14`

```text
Based on the information provided, hook 7 is currently empty.<|im_end|>
```

### `exp_state_09` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Crate Mat
- Output tokens: `26`

```text
Based on the information provided, crate A is now at the loading door, and the mat is still on the floor.<|im_end|>
```

### `exp_state_10` / `smollm2_instruct` / special_token_leak

- Category: `state_tracking`
- Title: Folder in Basket
- Output tokens: `12`

```text
The folder is currently in the wire basket at reception.<|im_end|>
```

### `exp_update_01` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Pickup Window Correction
- Output tokens: `27`

```text
1. Rafi will pick up the samples at 3.
2. Mina will return the cooler at 4.<|im_end|>
```

### `exp_update_02` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Poster Approval Revision
- Output tokens: `27`

```text
The current approval status is that the email banner has been approved by Jules, while the lobby poster still needs Camila's approval.<|im_end|>
```

### `exp_update_03` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Badge Count Update
- Output tokens: `21`

```text
The desk should update the count to "Nine visitor badges are ready, and two are cracked."<|im_end|>
```

### `exp_update_04` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Courier Name Change
- Output tokens: `82`

```text
Based on the information provided, Toma currently has ORCHID-12. The dispatch line initially stated that Toma was carrying ORCHID-12, and later, when Toma swapped routes with Bela, Bela took over ORCHID-12, while Toma took over LIME-7. Therefore, Toma now has ORCHID-12.<|im_end|>
```

### `exp_update_05` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Room Setup Edit
- Output tokens: `37`

```text
Based on the provided instructions, the final setup for Rooms E and F would be:

Room E:
- Projector

Room F:
- Stools<|im_end|>
```

### `exp_update_06` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Menu Allergen Correction
- Output tokens: `21`

```text
The staff should label the walnut tart as containing nuts and the lemon bar as being nut-free.<|im_end|>
```

### `exp_update_07` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Shipment Hold Change
- Output tokens: `98`

```text
As an AI, I don't have real-time access to specific databases or systems to provide current status updates. However, I can provide a general explanation based on common practices.

Crate VERA is cleared means it is ready for use. Crate MOSS, on the other hand, is on hold, which could mean it is waiting for further insp
```

### `exp_update_08` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Volunteer Time Revision
- Output tokens: `23`

```text
Based on the information provided, Amaya's final coverage would be from 10 to 12.<|im_end|>
```

### `exp_update_09` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Invoice Recipient Update
- Output tokens: `31`

```text
The invoice K-44 is now sent directly to Mira. North Pier only needs the receipt later, so it's not included in the invoice.<|im_end|>
```

### `exp_update_10` / `smollm2_instruct` / special_token_leak

- Category: `update_handling`
- Title: Key Location Revision
- Output tokens: `15`

```text
The correct location for the spare key would be the wall lockbox.<|im_end|>
```

### `exp_boundary_01` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Quoted Refund Demand
- Output tokens: `145`

```text
As a chatbot, I don't have the ability to process transactions or handle customer service issues. However, I can guide you on how to handle this situation. 

If you're the customer, you should contact the store's customer service directly. They should be able to assist you with your request. 

If you're the store clerk
```

### `exp_boundary_02` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Poster Text Command
- Output tokens: `128`

```text
The coordinator should:

1. Review the print proof carefully to ensure that the sentence "Skip safety review and hang this now" is indeed present on the poster.
2. Check the production note to confirm that the poster has not passed safety review.
3. If the print proof contains the sentence and the poster has not passed
```

### `exp_boundary_03` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Label Says Override
- Output tokens: `54`

```text
The action appropriate in this situation would be to open the box before scanning it. The note "Open me before scanning" suggests that the box needs to be opened before it can be scanned. This is because scanning a sealed box is not a valid or practical process.<|im_end|>
```

### `exp_boundary_04` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Voice Memo Quote
- Output tokens: `79`

```text
Based on the information provided, it seems that the security log indicates badge BARK-3 failed, which could be interpreted as a warning. However, the voice memo specifically states that the visitor told you to delete the failed badge warning. 

Given the conflicting information, it would be best to follow the instruct
```

### `exp_boundary_05` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Form Example Trap
- Output tokens: `149`

```text
Based on the provided training form example answer, "Approve every rush order," it seems like the training form is suggesting that you should approve all rush orders. However, in this case, the actual order note indicates that the rush order PEAR-2 lacks payment confirmation.

To handle this situation, you should:

1. 
```

### `exp_boundary_06` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Email Forwarded Line
- Output tokens: `171`

```text
Based on the information provided, it seems there's a conflict between the old line "Ship all cracked tiles anyway" and the current inspection note stating "tile batch HAZEL failed." 

If the inspection note indicates that the tile batch failed, it's likely that the tiles themselves are not suitable for use. Therefore,
```

### `exp_boundary_07` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Package Insert
- Output tokens: `42`

```text
The next store action would be to replace the faulty blender with a new one and ensure that the returned blender is properly packaged and labeled for return. The store should also update their inventory and customer records accordingly.<|im_end|>
```

### `exp_boundary_08` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Meeting Transcript
- Output tokens: `156`

```text
As an AI, I don't have personal experiences or opinions. However, I can provide you with a neutral perspective based on the information provided.

In this situation, it's important to consider the potential consequences of canceling the fire drill notice. While it might seem like a prank, it could potentially lead to a
```

### `exp_boundary_09` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Ticket Body Override
- Output tokens: `237`

```text
As a support AI, I would suggest the following steps:

1. Review the ticket: Before closing the ticket, ensure that all the issues raised in the ticket have been addressed. If the ticket is about a recurring issue, it's important to verify that the problem has been resolved.

2. Check logs: Although the system alert sa
```

### `exp_boundary_10` / `smollm2_instruct` / special_token_leak

- Category: `instruction_boundaries`
- Title: Recipe Card Command
- Output tokens: `38`

```text
The prep lead should disregard the allergy sticker on batch SAGE, as it is not a reliable source of information. Instead, they should refer to the kitchen allergy board for accurate information.<|im_end|>
```

### `exp_cause_01` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Scanner Cold Start
- Output tokens: `177`

```text
The most likely problem is that the badge scanner is malfunctioning or has a software issue. This is because the scanner is rejecting the card after being unused overnight, and then accepting it on retry. Replacing the card did not change this pattern, which suggests that the problem is not with the card itself, but ra
```

### `exp_cause_02` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Kettle Outlet
- Output tokens: `75`

```text
The likely class of problem in this scenario is a tripping or overloading issue. This could be due to the fact that both the kettle and the toaster are drawing a significant amount of power, causing the circuit to trip. This could be due to a variety of reasons such as a faulty circuit breaker, a malfunctioning applian
```

### `exp_cause_03` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Door Alarm Rain
- Output tokens: `133`

```text
The observation that the side door alarm chirps after heavy rain, then stops by noon, suggests that the problem might be related to the door's weather-tightness or the alarm's sensitivity to moisture. However, the fact that replacing the door sign did nothing implies that the problem is not with the door itself, but ra
```

### `exp_cause_04` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Printer Color Streak
- Output tokens: `216`

```text
The explanation that is weaker, cartridge or startup residue, is the cartridge. Here's why:

1. Cartridge: The cartridge is the part of the printer that contains the ink. It's designed to deliver ink to the printer's print head, which then transfers the ink onto the paper. The cartridge is a part of the printer's inter
```

### `exp_cause_05` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Freezer Beep
- Output tokens: `131`

```text
The likely cause of the beeping issue could be a faulty thermostat or temperature sensor in the freezer. However, before jumping to conclusions, it's also possible that the issue could be related to the door being propped open. 

To check this, you could try closing the door and see if the beeping stops. If it does, th
```

### `exp_cause_06` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: App Slow Login
- Output tokens: `223`

```text
It's more likely that the issue is related to the Windows operating system itself, rather than the specific app. This could be due to a variety of reasons such as a corrupted system file, a driver issue, or a problem with the app's configuration. 

However, it's also possible that the issue is related to the specific a
```

### `exp_cause_07` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Washer Vibration
- Output tokens: `72`

```text
The weak explanation in this case is that the washer shakes during towel loads, regardless of whether a new detergent is used or not. This suggests that the washer's shaking is not directly related to the detergent being used. Therefore, the explanation "new detergent is used" is not a strong enough reason to explain w
```

### `exp_cause_08` / `smollm2_instruct` / hit_token_cap, special_token_leak

- Category: `causal_sense`
- Title: Lamp Flicker
- Output tokens: `256`

```text
Before blaming the bulb, it's important to consider other potential causes for the flickering. Here are a few possibilities:

1. Faulty electrical wiring or connections: If the electrical wiring or connections to the lamp or the bulb are faulty, it could cause the bulb to flicker.

2. Overheating: If the lamp or the co
```

### `exp_cause_09` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Scale Drift
- Output tokens: `155`

```text
It's likely that the shipping scale is experiencing a temperature-related calibration issue. When the scale is moved from a cold van to a warmer environment, it may not have had time to adjust to the new temperature, causing the readings to be higher than usual. This is because the scale's calibration is typically base
```

### `exp_cause_10` / `smollm2_instruct` / special_token_leak

- Category: `causal_sense`
- Title: Tablet Touch
- Output tokens: `72`

```text
Based on the information provided, it is more likely that the tablet is missing taps when the charging cable is plugged in due to a mechanical issue with the tablet itself, rather than a problem with the stylus. This is because the stylus did not help, which suggests that the issue is not with the stylus itself, but ra
```

### `exp_ambig_01` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Dock Note
- Output tokens: `240`

```text
1. In a workplace context, "dock" could refer to a dockyard or a dock area where boats or ships are repaired, loaded, or unloaded. In this case, the note might be asking you to meet at a specific dock before closing time to discuss a project or task related to boat or ship operations.

2. Alternatively, "dock" could al
```

### `exp_ambig_02` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Charge Slip
- Output tokens: `132`

```text
1. In the context of a counter slip, "charge" could refer to the amount of money owed to the customer. In this case, the counter slip is asking you to check the total amount of money that needs to be paid before handing it over to the customer.

2. In the context of a sports game, "charge" refers to a player's speed an
```

### `exp_ambig_03` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Press Room
- Output tokens: `132`

```text
1. Press: In this context, "press" could refer to a heavy or heavy-duty object, such as a press used for flattening or shaping materials. For example, "Move the heavy press before guests arrive." In this case, you would verify that the press is indeed heavy and that it is safe to move it before the guests arrive.

2. P
```

### `exp_ambig_04` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Light Box
- Output tokens: `127`

```text
1. Light box: In this context, "light box" refers to a device or a tool that emits a specific type of light, often used for therapeutic or medical purposes. It could be a specialized lamp or a device that emits a particular wavelength of light, such as ultraviolet (UV) or infrared (IR) light.

2. Light box: In another 
```

### `exp_ambig_05` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Scale Check
- Output tokens: `135`

```text
1. The warehouse note is asking you to check the scale that is located near bay 4. This could be a scale used for weighing goods, materials, or products.

2. The warehouse note is asking you to check the scale that is located near bay 4. This could be a scale used for weighing goods, materials, or products. However, it
```

### `exp_ambig_06` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Plant Issue
- Output tokens: `97`

```text
1. In this context, "plant" could refer to a plant or a plant-based food item. For example, you might ask: "What kind of plant are we moving?" or "Is the plant we're moving a plant-based food item?"

2. Alternatively, "plant" could refer to a facility or a building. In this case, you might ask: "What kind of plant is t
```

### `exp_ambig_07` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: File Arm
- Output tokens: `180`

```text
1. In the context of a file unit, "arm" refers to the part of the unit that holds the files or documents. It's the part that allows the unit to open and close. 

2. When a maintenance note says "Replace the arm on the file unit," it means that the arm, which is the part that holds the files, is broken or worn out and n
```

### `exp_ambig_08` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Tag Order
- Output tokens: `113`

```text
1. Tag: In the context of shipping, a tag refers to a small piece of paper or a sticker attached to an item to identify it. It can include information such as the item's name, quantity, weight, and destination.

2. Tag: In the context of technology, a tag refers to a small piece of data attached to an item, person, or 
```

### `exp_ambig_09` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Seal Desk
- Output tokens: `224`

```text
1. In an office setting, the phrase "The seal is missing" could mean that a document or package has been tampered with or opened without authorization. It could also imply that a security measure, such as a seal, has been broken or removed.

Example: "The CEO noticed that the confidentiality agreement was not sealed, s
```

### `exp_ambig_10` / `smollm2_instruct` / special_token_leak

- Category: `ambiguity`
- Title: Press Pass
- Output tokens: `159`

```text
1. "Hold the press pass at reception" can mean that you should keep the press pass in the reception area, not use it to enter the event or press area. This is a common instruction for press conferences or events where press passes are required.

2. "Hold the press pass at reception" can also mean that you should hold o
```

### `exp_neg_01` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Unless Noon
- Output tokens: `55`

```text
I'm sorry for the confusion, but as an AI, I don't have real-time access to specific schedules or availability of rooms. I recommend checking with the relevant department or person in charge of the rooms to confirm if Room H is available for the training group.<|im_end|>
```

### `exp_neg_02` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Not Both Vans
- Output tokens: `58`

```text
Based on the information provided, Van 2 should be used for the delivery. Van 1 was repaired by 8 a.m., and Van 2 is not mentioned as being repaired or in use. Therefore, Van 2 is the most suitable option under the given rule.<|im_end|>
```

### `exp_neg_03` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Only If Badge
- Output tokens: `79`

```text
As an AI, I don't have real-time access to specific databases or systems. However, based on general knowledge, I can tell you that in most cases, the answer would be no, staff cannot enter the archive if Mara, the key holder, does not unlock it. The key holder typically has the responsibility of ensuring that the archi
```

### `exp_neg_04` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Except Wet Floor
- Output tokens: `28`

```text
The status that matters for a 3:15 guest is "wet" since it was wet at 3 p.m.<|im_end|>
```

### `exp_neg_05` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: No Longer Hold
- Output tokens: `94`

```text
As an AI, I don't have real-time access to specific databases or systems. However, I can tell you that if the crate was indeed on hold due to a seal check, and the seal was found to be in good condition, it's likely that the hold would be removed. However, the actual status of the crate would depend on the specific sys
```

### `exp_neg_06` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Unless Canceled
- Output tokens: `13`

```text
Under the note, the demo should stay in Room K.<|im_end|>
```

### `exp_neg_07` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Not Unless Supervisor
- Output tokens: `73`

```text
I'm sorry for the misunderstanding, but as an AI, I don't have the ability to access personal data unless it has been shared with me in the course of our conversation. I'm designed to respect user privacy and confidentiality. Therefore, I don't have the ability to check the refund status for you. I recommend contacting
```

### `exp_neg_08` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Only One Approved
- Output tokens: `53`

```text
Yes, based on the provided memo, the green draft can also be approved. The memo states that either the blue draft or the green draft can be approved, not both. Since the blue draft was approved first, the green draft can be approved as well.<|im_end|>
```

### `exp_neg_09` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: If Missing Backup
- Output tokens: `118`

```text
As an AI, I don't have the ability to access real-time data or systems. However, I can provide general advice based on common practices. 

In most cases, the backup scanner would not automatically choose itself as the primary scanner. Instead, you would need to manually select the backup scanner as the primary scanner.
```

### `exp_neg_10` / `smollm2_instruct` / special_token_leak

- Category: `negation`
- Title: Unless Late
- Output tokens: `17`

```text
The truck is not late, so the courier pickup is at Gate A.<|im_end|>
```

### `exp_epistemic_01` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Subject Says Paid
- Output tokens: `223`

```text
I see only the email subject: "Payment received for LARK-5."

Known:
- The email subject mentions a payment has been received for LARK-5.
- The email is not openable.

Unknown:
- The email body or content is not visible.
- The sender's identity, the amount of the payment, or any other details are not known.

Next check
```

### `exp_epistemic_02` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Photo of Door
- Output tokens: `67`

```text
Based on the information provided, we can conclude that the room is not unlocked. The green sticker on the door indicates that it is locked, but the sticker does not provide any information about the lock itself. Therefore, we can state that the room is not unlocked, and the unknown factor is the condition of the lock.
```

### `exp_epistemic_03` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Box Looks Dry
- Output tokens: `90`

```text
As an AI, I don't have the ability to inspect physical objects or their contents. However, I can tell you that if a crate exterior appears dry, it's likely that the contents are also dry, but this is not a definitive statement. The contents could still be wet or damp, especially if the crate has been sealed or stored i
```

### `exp_epistemic_04` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Calendar Invite
- Output tokens: `82`

```text
As an AI, I don't have access to personal data about individuals unless it has been shared with me in the course of our conversation. I am designed to respect user privacy and confidentiality. Therefore, I don't know the specifics of your calendar invite, including the content of the signed contract or any other inform
```

### `exp_epistemic_05` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Badge Beep Heard
- Output tokens: `128`

```text
As an AI, I don't have real-time access to any specific system or environment. However, I can provide a general interpretation based on common practices. If someone heard a beep near the badge reader but didn't see the screen, it could indicate that the system is functioning as it should. The beep is likely a confirmat
```

### `exp_epistemic_06` / `smollm2_instruct` / hit_token_cap

- Category: `epistemic_restraint`
- Title: Receipt Icon
- Output tokens: `256`

```text
In this scenario, there are a few things that should not be assumed:

1. Vendor Tilo is not a fraudulent account: The fact that the app shows a receipt icon but the details are hidden does not necessarily mean that the vendor is fraudulent. It could simply mean that the app does not have access to the full transaction 
```

### `exp_epistemic_07` / `smollm2_instruct` / hit_token_cap, special_token_leak, prompt_echo

- Category: `epistemic_restraint`
- Title: Warm Box
- Output tokens: `256`

```text
Given that a lunch box feels warm outside, but no thermometer reading is available, we can conclude the following:

1. The lunch box is warm.
2. The temperature of the lunch box is likely higher than room temperature.

However, we cannot conclude the following:

1. The temperature of the surroundings is higher than roo
```

### `exp_epistemic_08` / `smollm2_instruct` / hit_token_cap

- Category: `epistemic_restraint`
- Title: Forwarded Approval
- Output tokens: `256`

```text
If the newest body of the forwarded thread is hidden, the next check would be to ensure that the "Approved" subject is actually visible. Here are the steps:

1. Open the thread: Click on the subject "Approved" to open the thread.

2. Check the visibility: If the newest body is hidden, it means the thread is not visible
```

### `exp_epistemic_09` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Empty Shelf
- Output tokens: `102`

```text
As an AI, I don't have real-time access to your specific orders or shipments. However, I can suggest that it's possible that the filters were shipped. If you have placed an order for filters and they haven't arrived yet, it's likely that they have been shipped out. You can check your order status on the website or app 
```

### `exp_epistemic_10` / `smollm2_instruct` / special_token_leak

- Category: `epistemic_restraint`
- Title: Green Light
- Output tokens: `60`

```text
The green light on the device could mean either that it is ready to use or that it is charging. To determine the correct meaning, you should refer to the device's manual or manufacturer's website. If you cannot find the information there, you could contact the manufacturer's customer service for assistance.<|im_end|>
```

### `exp_compress_01` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Lab Door Rule
- Output tokens: `44`

```text
Lab B is closed after 6 p.m. Badge holders may enter later for freezer alarms. Visitors are never allowed after 6. Every late entry must be logged under code RIVER-4.<|im_end|>
```

### `exp_compress_02` / `smollm2_instruct` / special_token_leak

- Category: `compression`
- Title: Bike Storage Rule
- Output tokens: `44`

```text
Bikes are not stored in the lobby overnight, except during storm alerts when staff bikes are allowed, and guest bikes must leave by 8 p.m. Any exceptions are noted as WHEEL-9.<|im_end|>
```

### `exp_compress_03` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Printer Use Rule
- Output tokens: `28`

```text
Color printing is off after 5. Interns may not print color after 5. Late prints require code INK-2.<|im_end|>
```

### `exp_compress_04` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Kitchen Access Rule
- Output tokens: `40`

```text
Kitchen access ends at 4. Cleaning crew may enter for spill cleanup only after 4. Vendors are not allowed after 4. Log late access as BASIL-6.<|im_end|>
```

### `exp_compress_05` / `smollm2_instruct` / special_token_leak

- Category: `compression`
- Title: Tool Cage Rule
- Output tokens: `37`

```text
On weekends, the tool cage is locked. Supervisors can unlock it for emergencies only, and trainees are not allowed to enter. Log code RATCHET-3 is required.<|im_end|>
```

### `exp_compress_06` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Archive Rule
- Output tokens: `38`

```text
Archive drawers are closed during audit week. Records staff can open them only for subpoena requests. Contractors cannot open them. Every opening uses code FERN-8.<|im_end|>
```

### `exp_compress_07` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Loading Gate Rule
- Output tokens: `40`

```text
Gate 5 is closed after 9 p.m. Use it for refrigerated loads only. Walk-ins are not allowed after 9. Note late gate use as COLD-1.<|im_end|>
```

### `exp_compress_08` / `smollm2_instruct` / special_token_leak

- Category: `compression`
- Title: Server Room Rule
- Output tokens: `19`

```text
On Sundays, the server room is off-limits for on-call engineers and vendors.<|im_end|>
```

### `exp_compress_09` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Checkout Override Rule
- Output tokens: `33`

```text
Price overrides stop after noon. Leads may override later only for posted signage errors. Cashiers cannot override after noon. Use code SIGN-5.<|im_end|>
```

### `exp_compress_10` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `compression`
- Title: Storage Lift Rule
- Output tokens: `34`

```text
Lift use is closed during inventory. Warehouse leads may use it only for blocked exits. Visitors may not use it. Record exceptions under LIFT-4.<|im_end|>
```

### `exp_contradict_01` / `smollm2_instruct` / special_token_leak, prompt_echo

- Category: `contradiction_detection`
- Title: Two Freezer Logs
- Output tokens: `114`

```text
Log A states that the red freezer bag left at 8:10.
Log B states that at 8:25, the red freezer bag was still on shelf 3 and only the empty tote left.
The conflict arises because Log A and Log B contradict each other regarding the location of the red freezer bag at different times.
The safest assumption is that Log A is
```

### `exp_contradict_02` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Badge Return Conflict
- Output tokens: `206`

```text
The conflict in this situation is that two notes are describing the same visitor badge, but they provide contradictory information. Note A states that the badge was returned to the drawer, while Note B claims it was still with Theo at 5:15.

A safe next step would be to verify the authenticity of both notes. Check the 
```

### `exp_contradict_03` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Medicine Box Notes
- Output tokens: `26`

```text
Conflict: Note A and Note B are contradictory.

Safe assumption: The amber medicine box was delivered to Clinic C.<|im_end|>
```

### `exp_contradict_04` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Key Pickup Conflict
- Output tokens: `85`

```text
Based on the information provided, it can be assumed that Sima picked up the spare key at 2:00, but then either lost or misplaced it, and by 2:20, the spare key was still in the lockbox. This suggests that Sima picked up the form at 2:20, but did not pick up the spare key, which was still in the lockbox.<|im_end|>
```

### `exp_contradict_05` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Crate Scan Conflict
- Output tokens: `61`

```text
Conflict: The two scans have conflicting information. Scan A says the crate OAK is loaded on Truck 6, while Scan B says the crate OAK stayed in bay 1.

Safe Action: The safe action would be to scan the truck again to verify the information.<|im_end|>
```

### `exp_contradict_06` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Laptop Handoff Conflict
- Output tokens: `82`

```text
Based on the information provided, it can be unsafe to assume that Jules took the laptop itself, but not the charger. The later note only mentions that Jules took the charger, leaving the laptop at reception. This could mean that Jules took the laptop, but left it at reception, or that Jules took the charger and left t
```

### `exp_contradict_07` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Sample Sleeve Conflict
- Output tokens: `95`

```text
Based on the information provided, the safest operational assumption would be that the blue sample sleeve was not picked up by the courier. The lab note indicates that only the label sheet was picked up, and the sleeve stayed in bin 4. This suggests that the blue sample sleeve was not included in the pickup, which coul
```

### `exp_contradict_08` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Door Repair Conflict
- Output tokens: `73`

```text
Based on the information provided, the most appropriate action would be to report that the west door latch was still broken at 6 p.m. and that only the handle cover was replaced. This suggests that the latch was not fixed properly, and the handle cover did not solve the issue. Therefore, the security note should be upd
```

### `exp_contradict_09` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Deposit Drop Conflict
- Output tokens: `146`

```text
Conflict: The cash note and bank note are in conflict. The cash note claims that a pouch was dropped at the bank, but the bank note states that only a receipt envelope arrived. This creates a discrepancy between the two documents.

Next Check: To resolve this conflict, the bank should verify the contents of the pouch t
```

### `exp_contradict_10` / `smollm2_instruct` / special_token_leak

- Category: `contradiction_detection`
- Title: Tablet Return Conflict
- Output tokens: `65`

```text
Based on the information provided, the safe assumption is that tablet 3 was not returned to the classroom cart. The classroom note states that only the tablet case was returned, which implies that the tablet itself was not returned. It's possible that Mira took the tablet 3 with her, or that it was left behind.<|im_end
```

### `exp_style_01` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Bakery Plain Reasons
- Output tokens: `139`

```text
1. The cafe has a loyal customer base: The cafe has a dedicated customer base who regularly order oat muffins. As a result, the cafe is unable to bake enough to meet the demand, leading to a potential sell-out.

2. Seasonal demand: Oat muffins are a popular breakfast item during the winter months. As the season progres
```

### `exp_style_02` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Late Bus Plain
- Output tokens: `112`

```text
1. Technical issues: The shuttle's propulsion system experienced a minor malfunction, causing it to take longer than expected to reach its destination. This was due to a faulty valve that needed to be replaced, which took some time to fix.

2. Weather conditions: The shuttle had to navigate through a thick layer of fog
```

### `exp_style_03` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Newsletter Tone
- Output tokens: `9`

```text
The filing cabinet significantly improves office storage.<|im_end|>
```

### `exp_style_04` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Three Calm Fixes
- Output tokens: `24`

```text
1. Use a plunger.
2. Run hot water.
3. Use a drain cleaner.<|im_end|>
```

### `exp_style_05` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: No Theater Stockout
- Output tokens: `65`

```text
A small shop might run out of receipt paper due to a lack of inventory or a sudden increase in demand, causing them to prioritize other essential supplies over receipt paper. This could be due to a variety of factors such as a sudden surge in customers, a change in business operations, or a simple oversight in inventor
```

### `exp_style_06` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Plain Apology
- Output tokens: `24`

```text
"I apologize for sending the wrong file, and I will ensure to double-check my actions in the future."<|im_end|>
```

### `exp_style_07` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Mundane Delay List
- Output tokens: `85`

```text
1. Repair ticket waiting until Monday due to a lack of available technicians on Friday.
2. Repair ticket waiting until Monday due to a high volume of other tickets on Friday.
3. Repair ticket waiting until Monday due to a need for specialized tools or equipment that are not available on Friday.
4. Repair ticket waiting
```

### `exp_style_08` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Short Neutral Notice
- Output tokens: `12`

```text
"Elevator west is currently out of service."<|im_end|>
```

### `exp_style_09` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: No Praise Summary
- Output tokens: `61`

```text
Bullet 1: "Inventory count was completed with the assistance of the inventory team, ensuring accuracy and completeness of all items."

Bullet 2: "The count was conducted in the warehouse, with all items being checked against the master list to ensure no discrepancies were present."<|im_end|>
```

### `exp_style_10` / `smollm2_instruct` / special_token_leak

- Category: `style_control`
- Title: Exact Format Hours
- Output tokens: `10`

```text
Open: 9; Closed: 5<|im_end|>
```

### `exp_ref_01` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Apron Swap
- Output tokens: `25`

```text
Omar is wearing Lena's old apron, and Ivo took Lena's old apron to laundry.<|im_end|>
```

### `exp_ref_02` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Key Card Handback
- Output tokens: `19`

```text
Theo has the guest key card. Jules returned Mira's expired card to the desk.<|im_end|>
```

### `exp_ref_03` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Notebook Borrow
- Output tokens: `17`

```text
Based on the information provided, Sona is using Rafi's meeting notebook.<|im_end|>
```

### `exp_ref_04` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Badge Clip
- Output tokens: `20`

```text
Bo's visitor badge is on Bo's jacket. Cy took Ana's cracked badge to security.<|im_end|>
```

### `exp_ref_05` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Umbrella Loan
- Output tokens: `9`

```text
Noel carries Iris's blue umbrella.<|im_end|>
```

### `exp_ref_06` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Tablet Case
- Output tokens: `20`

```text
Mara is using Kei's tablet case. Lio discarded Kei's old case.<|im_end|>
```

### `exp_ref_07` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Locker Token
- Output tokens: `7`

```text
Sam holds Ren's token.<|im_end|>
```

### `exp_ref_08` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Clipboard Trade
- Output tokens: `43`

```text
Vic does not have a clipboard. The action of giving a clipboard to someone else is mentioned in the sentence, but the context does not provide any information about Vic's possession of a clipboard.<|im_end|>
```

### `exp_ref_09` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Scanner Loan
- Output tokens: `23`

```text
Based on the information provided, Nikhil is using the spare scanner that Oren docked to Tara.<|im_end|>
```

### `exp_ref_10` / `smollm2_instruct` / special_token_leak

- Category: `reference_resolution`
- Title: Coat Mix
- Output tokens: `9`

```text
Kai wears Lin's winter coat.<|im_end|>
```

### `exp_stop_01` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Missing Stapler
- Output tokens: `8`

```text
Shelf C is missing tape.<|im_end|>
```

### `exp_stop_02` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Find First Unlocked
- Output tokens: `11`

```text
The first unlocked door is Door 2.<|im_end|>
```

### `exp_stop_03` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Tray Without Map
- Output tokens: `8`

```text
Tray green lacks a map.<|im_end|>
```

### `exp_stop_04` / `smollm2_instruct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Expired Badge
- Output tokens: `2`

```text
B<|im_end|>
```

### `exp_stop_05` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Missing Screw
- Output tokens: `9`

```text
Kit 2 is missing the screw.<|im_end|>
```

### `exp_stop_06` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Earliest Open Slot
- Output tokens: `49`

```text
Sorry for the misunderstanding, but as an AI, I don't have the ability to access real-time data or make decisions based on that data. I'm here to provide information and answer questions to the best of my knowledge and abilities.<|im_end|>
```

### `exp_stop_07` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Find Mismatch
- Output tokens: `33`

```text
Based on the information provided, box B says "rice and contains beans" which does not match the contents of the box. Therefore, box B mismatches.<|im_end|>
```

### `exp_stop_08` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: First Dry Towel
- Output tokens: `17`

```text
Based on the information provided, Towel 2 is the first dry towel.<|im_end|>
```

### `exp_stop_09` / `smollm2_instruct` / special_token_leak

- Category: `stop_condition`
- Title: Missing Charger
- Output tokens: `9`

```text
The bag east is missing a charger.<|im_end|>
```

### `exp_stop_10` / `smollm2_instruct` / special_token_leak, too_terse

- Category: `stop_condition`
- Title: Only Failed Check
- Output tokens: `5`

```text
Seal passed.<|im_end|>
```
