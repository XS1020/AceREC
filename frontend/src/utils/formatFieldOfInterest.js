const idsOfTier0 = require('../assets/data/V0_to_V1.json')
const tagsOfTier0 = require('../assets/data/V0_Field_INFO.json')
const tagsOfTier1 = require('../assets/data/V1_Field_INFO.json')
export default function () {
    const fieldOfInterest = {}
    for (const key of Object.keys(idsOfTier0)) {
        const children = JSON.parse(JSON.stringify(idsOfTier0[key]))
        let id
        for (let i = 0; i < children.length; i++) {
            id = parseInt(children[i])
            children[i] = {
                id, name: tagsOfTier1[id]
            }
        }
        fieldOfInterest[parseInt(key)] = {
            name: tagsOfTier0[key],
            children
        }
    }
    return fieldOfInterest
}